import copy
import logging
import os
from functools import partial
from typing import Literal

import mlflow
import numpy as np
import torch.distributed as dist
from huggingface_hub._login import _login as hf_login
from peft import LoraConfig
from torch import nn
from transformers import EarlyStoppingCallback, PreTrainedModel, Trainer
from trl import SFTConfig, SFTTrainer

from giotto_llm.consts import ROOT_PATH
from giotto_llm.data import Dataset
from giotto_llm.finetuning.__main__ import get_eval_dataset, get_sft_config, get_train_dataset
from giotto_llm.finetuning.args import parse_arguments_main
from giotto_llm.finetuning.utils import MAP_WRAPPER, FinetuningConfig
from giotto_llm.prompts.consts import TYPES_OF_PROMPTS
from giotto_llm.prompts.grid_formatter import GridFormatter
from giotto_llm.reader import ReaderMany, ReaderPickle
from giotto_llm.transforms import transform_task
from giotto_llm.utils import is_tf32_supported, split_tasks_by_test, write_json


def prepare_model(model: PreTrainedModel) -> None:
    # Only finetune head and embedding
    for param in model.parameters():
        param.requires_grad_(False)
    # Need to dequantize trainable parameters to avoid using adaptors
    # For Qwen lm_head and embed_tokens is the same tensor
    input_embeddings = model.get_input_embeddings()
    output_embeddings = model.get_output_embeddings()
    # Some models use custom layers
    for embedding in (input_embeddings, output_embeddings):
        for param in embedding.parameters():
            param.requires_grad_(True)


def main(logger: logging.Logger, config: FinetuningConfig) -> None:
    """Train embedding and classifier layers of model"""
    if not os.path.exists(config.output_dir):
        os.mkdir(config.output_dir)

    wrapper_cls = MAP_WRAPPER[config.wrapper]
    sft_config = get_sft_config(config=config, log_mlflow=False)

    logger.info("Initializing model")
    wrapper = wrapper_cls(model_id=config.model_id, quantization=config.quantization)

    logger.info("Creating training dataset")
    train_dataset = get_train_dataset(
        config=config, model_type=wrapper.model_type, grid_formatter=wrapper.grid_formatter
    )
    # Create augmented evaluation set
    logger.info("Creating evaluation dataset")
    eval_dataset = get_eval_dataset(
        config=config,
        size=len(train_dataset) // 5,
        model_type=wrapper.model_type,
        grid_formatter=wrapper.grid_formatter,
    )

    if config.padding_side is not None:
        wrapper.tokenizer.padding_side = config.padding_side

    callbacks = [EarlyStoppingCallback(early_stopping_patience=config.early_stopping_patience)]

    prepare_model(wrapper.model)

    trainer = SFTTrainer(
        model=wrapper.model,
        args=sft_config,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=partial(wrapper.collate_fn_train, mask_inputs=not config.disable_input_mask),
        callbacks=callbacks,
    )
    logger.info("Training model")
    trainer.train()

    # Sync processes
    if dist.is_available() and dist.is_initialized():
        dist.barrier()
    if is_main_process():
        logger.info("Saving model")
        trainer.model.to("cpu")
        wrapper.save_pretrained(config.output_dir)


def is_main_process() -> bool:
    return "RANK" not in os.environ or int(os.environ["RANK"]) == 0


if __name__ == "__main__":
    if "HF_TOKEN" in os.environ:
        HF_TOKEN = os.environ["HF_TOKEN"]
        hf_login(token=HF_TOKEN, add_to_git_credential=False)
    args = parse_arguments_main()
    config = FinetuningConfig(
        model_id=args["model_id"],
        wrapper=args["wrapper"],
        output_dir=args["output_dir"],
        quantization="no",
        dataset=args["dataset"],
        transform_background_color=args["transform_background_color"],
        compress_colors=args["compress_colors"],
        learning_rate=args["learning_rate"],
        per_device_batch_size=args["batch_size"],
        gradient_accumulation_steps=args["gradient_accumulation_steps"],
        num_train_epochs=args["num_train_epochs"],
        neftune_noise_alpha=args["neftune_noise_alpha"],
        padding_side=args["padding_side"],
        prompt_type=args["prompt_type"],
        training_set_size=args["training_set_size"],
        evaluation_set_size=args["evaluation_set_size"],
        logging_steps=args["logging_steps"],
        eval_steps=args["eval_steps"],
        low_memory=args["low_memory"],
        early_stopping_patience=args["early_stopping_patience"],
        save_total_limit=args["save_total_limit"],
        disable_input_mask=args["disable_input_mask"],
        gradient_checkpointing=args["gradient_checkpointing"],
    )
    main(logger=args["logger"], config=config)
