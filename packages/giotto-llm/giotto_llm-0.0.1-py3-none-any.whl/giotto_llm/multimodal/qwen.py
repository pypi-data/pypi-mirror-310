import json
import os
from typing import Any, List, Literal, Optional, Tuple, Union

import torch
from accelerate import PartialState
from qwen_vl_utils import process_vision_info
from torch import Tensor
from torch.nn import CrossEntropyLoss
from transformers import (
    AutoConfig,
    BitsAndBytesConfig,
    Qwen2VLForConditionalGeneration,
    Qwen2VLProcessor,
)
from transformers.models.qwen2_vl.modeling_qwen2_vl import Qwen2VLCausalLMOutputWithPast

from ..prompts.grid_formatter import GridFormatter
from ..transforms import Transforms, _BackTransformTestOutput
from ..type_aliases import JSONTask, OAIMessage
from ..utils import BNBConfig, is_launched_with_torchrun
from ..wrapper import ModelWrapper


class _Qwen2VLForConditionalGeneration(Qwen2VLForConditionalGeneration):
    """There's a multi-gpu bug in the forward method, so override to fix."""

    def forward(
        self,
        input_ids: torch.LongTensor = None,  # type: ignore
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        pixel_values: Optional[torch.Tensor] = None,
        pixel_values_videos: Optional[torch.FloatTensor] = None,
        image_grid_thw: Optional[torch.LongTensor] = None,
        video_grid_thw: Optional[torch.LongTensor] = None,
        rope_deltas: Optional[torch.LongTensor] = None,
    ) -> Union[Tuple, Qwen2VLCausalLMOutputWithPast]:

        output_attentions = (
            output_attentions if output_attentions is not None else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if inputs_embeds is None:
            inputs_embeds = self.model.embed_tokens(input_ids)
            if pixel_values is not None:
                pixel_values = pixel_values.type(self.visual.get_dtype())
                image_embeds = self.visual(pixel_values, grid_thw=image_grid_thw)
                image_mask = (
                    (input_ids == self.config.image_token_id).unsqueeze(-1).expand_as(inputs_embeds)
                )
                # NOTE: Bugfix in below line
                image_mask = image_mask.to(inputs_embeds.device)
                image_embeds = image_embeds.to(inputs_embeds.device, inputs_embeds.dtype)
                inputs_embeds = inputs_embeds.masked_scatter(image_mask, image_embeds)  # type: ignore

            if pixel_values_videos is not None:
                pixel_values_videos = pixel_values_videos.type(self.visual.get_dtype())
                video_embeds = self.visual(pixel_values_videos, grid_thw=video_grid_thw)
                video_mask = (
                    (input_ids == self.config.video_token_id).unsqueeze(-1).expand_as(inputs_embeds)
                )
                video_embeds = video_embeds.to(inputs_embeds.device, inputs_embeds.dtype)
                inputs_embeds = inputs_embeds.masked_scatter(video_mask, video_embeds)  # type: ignore

            if attention_mask is not None:
                attention_mask = attention_mask.to(inputs_embeds.device)

        outputs = self.model(
            input_ids=None,
            position_ids=position_ids,
            attention_mask=attention_mask,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        hidden_states = outputs[0]
        logits = self.lm_head(hidden_states)
        logits = logits.float()

        loss = None
        if labels is not None:
            # Shift so that tokens < n predict n
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Enable model parallelism
            shift_labels = shift_labels.to(shift_logits.device)
            loss = loss_fct(shift_logits, shift_labels)

        if not return_dict:
            output = (logits,) + outputs[1:]
            return (loss,) + output if loss is not None else output

        return Qwen2VLCausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            rope_deltas=rope_deltas,
        )


class QwenVLWrapper(ModelWrapper):
    """Wrapper for Qwen2VL models."""

    model_type = "image-text-to-text"
    _target_modules = [
        "qkv",
        "attn.proj",
        "fc1",
        "fc2",
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "embed_tokens",  # lm_head is the same tensor as embed_tokens
    ]

    def __init__(
        self,
        model_id: str = "Qwen/Qwen2-VL-2B-Instruct",
        gpu_index: int = 0,
        quantization: (
            Literal[
                "no",
                "4bit-nf4",
                "4bit-dq-nf4",
                "4bit-fp4",
                "4bit-dq-fp4",
                "8bit-6",
                "8bit-5",
                "8bit-4",
            ]
            | None
        ) = None,
        config: dict[str, Any] = {},
    ):
        if quantization is None:
            quantization = "4bit-dq-nf4"
        # Increase the max supported number of tokens
        model_config = AutoConfig.from_pretrained(model_id)
        model_config.max_position_embeddings = max(
            model_config.max_position_embeddings, self._min_max_position_embeddings
        )
        # Merge default config with the given one
        config = {
            "quantization_config": BNBConfig[quantization],
            "device_map": (
                {"": PartialState().process_index}
                if is_launched_with_torchrun()
                else {"": f"cuda:{gpu_index}"}
            ),
            "config": model_config,
            "torch_dtype": "auto",  # If set to None, this can cause nan issues in log-likelihoods (due to fp16)
        } | config

        self.model_id = model_id
        self.model = _Qwen2VLForConditionalGeneration.from_pretrained(
            model_id,
            **config,
        )
        self.processor = Qwen2VLProcessor.from_pretrained(
            model_id,
        )
        self.tokenizer = self.processor.tokenizer
        self.generation_prompt_token_ids = self._get_generation_prompt_token_ids()
        self._init_grid_formatter_and_update_tokenizer_model()
        self._set_output_token_ids()
        self._init_sanity_checks()

    def collate_fn_eval(
        self,
        examples: list[tuple[OAIMessage, JSONTask, dict[str, Any], int, _BackTransformTestOutput]],
    ) -> dict[str, dict[str, Any] | list[int] | list[_BackTransformTestOutput] | list[JSONTask]]:
        """Data collator to encode text and image pairs."""
        conversation = [example[0][:2] for example in examples]
        text = self.processor.apply_chat_template(
            conversation, tokenize=False, add_generation_prompt=True
        )
        image_inputs = process_vision_info(conversation)[0]
        ## Tokenize the texts and process the images
        batch_inputs = self.processor(
            text=text, images=image_inputs, return_tensors="pt", padding=True, truncation=False
        )

        batch_indices = [example[2] for example in examples]
        backtransforms = [example[3] for example in examples]
        transformed_tasks = [example[1] for example in examples]

        return {
            "batch_inputs": batch_inputs,
            "batch_indices": batch_indices,
            "backtransforms": backtransforms,
            "transformed_tasks": transformed_tasks,
        }

    def collate_fn_train(
        self,
        examples: list[tuple[OAIMessage, JSONTask, int, _BackTransformTestOutput]],  # type: ignore
        mask_inputs: bool = True,
    ) -> dict[str, Tensor]:
        """The collate function."""
        assert all(example[0][2]["content"][0]["text"] != "" for example in examples)

        conversation = [example[0] for example in examples]
        text = self.processor.apply_chat_template(
            conversation, tokenize=False, add_generation_prompt=False
        )
        image_inputs = process_vision_info(conversation)[0]
        ## Tokenize the texts and process the images
        batch: dict[str, Tensor] = self.processor(
            text=text, images=image_inputs, return_tensors="pt", padding=True, truncation=False
        )
        batch["labels"] = self._create_labels(batch["input_ids"])
        return batch
