from __future__ import annotations

import json
import os
from typing import Any

import torch
from transformers import BitsAndBytesConfig

from .consts import MAX_GRID_SIZE
from .type_aliases import JSONTask


class RepeatSampler:
    """Utility sampler to avoid looping over a dataloader multiple times"""

    def __init__(self, n_repeats: int, size: int):
        self.n_repeats = n_repeats
        self.end = n_repeats * size
        self.current = 0

    def __len__(self) -> int:
        return self.end

    def __iter__(self) -> RepeatSampler:
        return self

    def __next__(self) -> int:
        if self.current < self.end:
            self.current += 1
            return (self.current - 1) // self.n_repeats
        raise StopIteration


def split_tasks_by_test(tasks: dict[str, JSONTask]) -> dict[str, JSONTask]:
    """Split tasks that have more than 1 test example.

    Also removes tasks that have too large grids
    """
    split_tasks: dict[str, JSONTask] = {}
    for task_id, task in tasks.items():
        n_test = len(task["test"])
        max_grid_side_length = _get_max_grid_side_length(task)
        if max_grid_side_length > MAX_GRID_SIZE:
            continue
        if n_test == 1:
            split_tasks[task_id] = task
            continue
        split_tasks |= {
            f"{task_id}-|-{i}": subtask for i, subtask in enumerate(split_single_task_by_test(task))
        }
    return split_tasks


def _get_max_grid_side_length(task: JSONTask) -> int:
    max_grid_side = 0
    for train_test in task:
        for pair in task[train_test]:
            for input_output in pair:
                max_grid_side = max(max_grid_side, len(pair[input_output]))
                max_grid_side = max(max_grid_side, len(pair[input_output][0]))
    return max_grid_side


def split_single_task_by_test(task: JSONTask) -> list[JSONTask]:
    split_tasks = []
    for test_pair in task["test"]:
        split_task: JSONTask = {"train": task["train"], "test": [test_pair]}
        split_tasks.append(split_task)
    return split_tasks


def is_tf32_supported() -> bool:
    # Check if CUDA is available
    if torch.cuda.is_available():
        # Get the current GPU device
        device = torch.cuda.current_device()

        # Get the device properties
        props = torch.cuda.get_device_properties(device)

        # Check for Ampere architecture (compute capability 8.x)
        if props.major >= 8:
            return True
        else:
            return False
    else:
        return False


def get_half_precision_dtype() -> torch.dtype:
    if is_tf32_supported() is True:
        return torch.bfloat16
    return torch.float16


def is_launched_with_torchrun() -> bool:
    # Check for environment variables set by torchrun
    return all(var in os.environ for var in ["RANK", "WORLD_SIZE", "LOCAL_RANK"])


def write_json(data: Any, filename: str) -> None:
    """Write json file."""
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=None)


BNBConfig = {
    "no": None,
    "4bit-nf4": BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=get_half_precision_dtype(),
    ),
    "4bit-dq-nf4": BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=get_half_precision_dtype(),
    ),
    "4bit-fp4": BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="fp4",
        bnb_4bit_compute_dtype=get_half_precision_dtype(),
    ),
    "4bit-dq-fp4": BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="fp4",
        bnb_4bit_compute_dtype=get_half_precision_dtype(),
    ),
    "8bit-6": BitsAndBytesConfig(load_in_8bit=True, llm_int8_threshold=6.0),
    "8bit-5": BitsAndBytesConfig(load_in_8bit=True, llm_int8_threshold=5.0),
    "8bit-4": BitsAndBytesConfig(load_in_8bit=True, llm_int8_threshold=4.0),
}
