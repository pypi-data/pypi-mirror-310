import logging
import pathlib
import random
from typing import Any

import numpy as np
from transformers import AutoTokenizer

from giotto_llm.consts import TYPES_OF_TRANSFORMS
from giotto_llm.prompts.consts import TYPES_OF_PROMPTS
from giotto_llm.prompts.grid_formatter import GridFormatter
from giotto_llm.transforms import transform_task
from giotto_llm.type_aliases import JSONTask
from giotto_llm.utils import split_tasks_by_test


class MessagesGenerator:
    """Generate `m` `Messages` for fine-tuning LLMs from `n` `JSONTask`s.

    Notes
    -----
    - Each task is augmented with a `Transforms` object.
    - Only `Messages` containing less than `max_seq_length` tokens are returned.
    - Multiple prompt types are allowed.
    """

    def __init__(
        self,
        path_to_tokenizer: AutoTokenizer,
        max_seq_length: int,
        prompts_with_weights: dict[str, int],
        transforms_with_weights: dict[str, int],
        logger: logging.Logger,
    ) -> None:
        abs_path_to_tokenizer = pathlib.Path(path_to_tokenizer).resolve(strict=True)
        assert abs_path_to_tokenizer.exists(), f"{abs_path_to_tokenizer=} does not exist"

        self.tokenizer = AutoTokenizer.from_pretrained(str(abs_path_to_tokenizer))
        self.max_seq_length = max_seq_length
        self.logger = logger

        for prompt_type, weight in prompts_with_weights.items():
            if prompt_type not in TYPES_OF_PROMPTS:
                self.logger.error(f"{prompt_type=} is not valid")
                raise ValueError(f"{prompt_type=} is not valid")
            if weight <= 0:
                self.logger.error(f"{weight=} needs to be greater than 0")
                raise ValueError(f"{weight=} needs to be greater than 0")

        for transform_type, weight in transforms_with_weights.items():
            if transform_type not in TYPES_OF_TRANSFORMS:
                self.logger.error(f"{transform_type=} is not valid")
                raise ValueError(f"{transform_type=} is not valid")
            if weight <= 0:
                self.logger.error(f"{weight=} needs to be greater than 0")
                raise ValueError(f"{weight=} needs to be greater than 0")

        # Prepare transforms and their weights
        all_transforms = []
        transforms_weights = np.zeros(shape=len(transforms_with_weights), dtype=np.float64)
        for idx, (tra, tra_weight) in enumerate(transforms_with_weights.items()):
            all_transforms.append(tra)
            transforms_weights[idx] = float(tra_weight)
        transforms_weights = transforms_weights / np.sum(transforms_weights)

        self.all_transforms = [TYPES_OF_TRANSFORMS[x] for x in all_transforms]
        self.transforms_weights = transforms_weights

        # Prepare prompts and their weights
        all_prompts_fn = []
        prompts_weights = np.zeros(shape=len(prompts_with_weights), dtype=np.float64)
        for idx, (p_fn, p_weight) in enumerate(prompts_with_weights.items()):
            all_prompts_fn.append(p_fn)
            prompts_weights[idx] = float(p_weight)
        prompts_weights = prompts_weights / np.sum(prompts_weights)

        self.all_prompts_fn = [
            TYPES_OF_PROMPTS[x](grid_formatter=GridFormatter()) for x in all_prompts_fn
        ]
        self.prompts_weights = prompts_weights

    def __call__(
        self,
        tasks: dict[str, JSONTask],
        num_messages_to_generate: int = 10,
        random_seed: int = 0,
    ) -> list[dict[str, Any]]:
        """Generate exactly `num_messages_to_generate` using the given `tasks`."""
        output: list[dict[str, Any]] = []
        tasks = split_tasks_by_test(tasks)
        sorted_task_ids = sorted(tasks.keys())
        num_tasks = len(sorted_task_ids)

        # Set random seeds
        random.seed(random_seed)
        np.random.seed(random_seed)

        # Loop until `num_messages_to_generate` are generated
        current_idx = 0
        num_messages_already_generated = 0
        MAX_RETRIES = 100
        num_retries = 0
        while (num_messages_already_generated < num_messages_to_generate) and (
            num_retries < MAX_RETRIES
        ):
            task_id_index = current_idx % num_tasks
            current_idx += 1
            task_id = sorted_task_ids[task_id_index]
            if current_idx % 50 == 0:  # Note: limiting logging output
                self.logger.info(
                    f">>> Generated: {num_messages_already_generated} | {task_id_index=} | {task_id[:10]=}"
                )

            # Select a random Transforms object, sampling with weights
            # Then apply it to obtain an augmented task
            random_index_transforms = int(
                np.random.choice(
                    np.arange(len(self.all_transforms)), size=1, p=self.transforms_weights
                )[0]
            )
            transforms = self.all_transforms[random_index_transforms]
            transformed_task, _ = transform_task(
                tasks[task_id],
                transforms=transforms,
            )

            # Select a random TextPromptBase object, sampling with weights
            # Then apply it to obtain Messages, which can be tokenized after applying
            # a chat template to them. We threshold on the length of the tokenized text
            random_index_prompt = int(
                np.random.choice(
                    np.arange(len(self.all_prompts_fn)), size=1, p=self.prompts_weights
                )[0]
            )
            prompts_fn = self.all_prompts_fn[random_index_prompt]
            messages = prompts_fn(transformed_task, 0)
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )

            length_tokenized_text = len(self.tokenizer.encode(text))
            if length_tokenized_text < self.max_seq_length:
                output.append(
                    {
                        "messages": messages,
                        "prompt_type": str(prompts_fn),
                        "transforms": transforms.dict(),
                        "tokenizer_id": self.tokenizer.name_or_path,
                        "length_tokenized_text": length_tokenized_text,
                        "task": transformed_task,
                    }
                )
                num_retries = 0
                num_messages_already_generated += 1
            else:
                num_retries += 1

        return output
