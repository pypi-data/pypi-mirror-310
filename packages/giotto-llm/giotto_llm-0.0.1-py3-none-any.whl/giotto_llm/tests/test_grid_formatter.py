import json
import logging
import os
from pathlib import Path

import pytest
from transformers import AutoTokenizer

from giotto_llm.consts import (
    C0,
    C1,
    C2,
    C3,
    C4,
    C5,
    C6,
    C7,
    C8,
    C9,
    DEFAULT_END_EXAMPLE_TOKEN,
    DEFAULT_END_INPUT_TOKEN,
    DEFAULT_END_OUTPUT_TOKEN,
    DEFAULT_END_ROW_TOKEN,
    DEFAULT_START_EXAMPLE_TOKEN,
    DEFAULT_START_INPUT_TOKEN,
    DEFAULT_START_OUTPUT_TOKEN,
    DEFAULT_START_ROW_TOKEN,
    GRID_FORMATTER_CONFIG_FILENAME,
)
from giotto_llm.prompts.grid_formatter import GridFormatter
from giotto_llm.transforms import _estimate_n_tokens_per_pair
from giotto_llm.type_aliases import Grid, JSONTask

path_to_llama_tokenizer = Path(__file__).parent / "llama_tokenizer"
llama_tokenizer = AutoTokenizer.from_pretrained(
    path_to_llama_tokenizer,
    trust_remote_code=False,
)

TEST_DIR = Path(__file__).parent


@pytest.mark.parametrize("tokenizer", (llama_tokenizer,))
def test_special_tokens(tokenizer: AutoTokenizer) -> None:
    grid_formatter = GridFormatter()

    additional_special_tokens = grid_formatter.get_special_tokens_not_in(tokenizer)

    assert "" not in additional_special_tokens

    default_special_tokens = [
        DEFAULT_START_EXAMPLE_TOKEN,
        DEFAULT_END_EXAMPLE_TOKEN,
        DEFAULT_START_INPUT_TOKEN,
        DEFAULT_END_INPUT_TOKEN,
        DEFAULT_START_OUTPUT_TOKEN,
        DEFAULT_END_OUTPUT_TOKEN,
        DEFAULT_START_ROW_TOKEN,
        DEFAULT_END_ROW_TOKEN,
        C0,
        C1,
        C2,
        C3,
        C4,
        C5,
        C6,
        C7,
        C8,
        C9,
    ]

    for token in default_special_tokens:
        if token not in tokenizer.vocab and token != "":
            assert token in additional_special_tokens


@pytest.mark.parametrize(
    "grid, input_or_output",
    [
        ([[1, 2], [3, 4]], "input"),
        ([[1, 2], [3, 4]], "output"),
        ([[0], [0]], "output"),
    ],
)
def test_encode_decode_v1(grid: Grid, input_or_output: str) -> None:
    grid_formatter = GridFormatter()

    encoded_grid = grid_formatter.encode_grid(grid=grid, input_or_output=input_or_output)
    logger = logging.Logger(__file__)
    decoded_grid = grid_formatter.decode_grid(
        encoded_grid, input_or_output=input_or_output, logger=logger
    )

    assert grid == decoded_grid


def test_to_dict() -> None:
    grid_formatter = GridFormatter()
    dict_representation = grid_formatter.to_dict()

    assert dict_representation == {
        "sE_token": DEFAULT_START_EXAMPLE_TOKEN,
        "eE_token": DEFAULT_END_EXAMPLE_TOKEN,
        "sI_token": DEFAULT_START_INPUT_TOKEN,
        "eI_token": DEFAULT_END_INPUT_TOKEN,
        "sO_token": DEFAULT_START_OUTPUT_TOKEN,
        "eO_token": DEFAULT_END_OUTPUT_TOKEN,
        "sR_token": DEFAULT_START_ROW_TOKEN,
        "eR_token": DEFAULT_END_ROW_TOKEN,
        "c0": C0,
        "c1": C1,
        "c2": C2,
        "c3": C3,
        "c4": C4,
        "c5": C5,
        "c6": C6,
        "c7": C7,
        "c8": C8,
        "c9": C9,
        "color_separator_token": "",
    }


def test_save() -> None:
    grid_formatter = GridFormatter()
    output_dir = str(TEST_DIR / "tmp_grid_formatter")
    grid_formatter.save(output_dir=output_dir)

    path_to_config = os.path.join(output_dir, GRID_FORMATTER_CONFIG_FILENAME)
    assert os.path.exists(path_to_config)

    with open(path_to_config, "r") as f:
        saved_grid_formatter_config = json.load(f)

    saved_grid_formatter = GridFormatter(**saved_grid_formatter_config)
    assert grid_formatter == saved_grid_formatter


def test_size(tasks: dict[str, JSONTask]) -> None:
    """Test that the size is as expected"""
    task_id = "fafffa47"
    task = tasks[task_id]
    # Use single char special tokens to make it easy to find length
    grid_formatter = GridFormatter(
        sE_token="a",
        eE_token="b",
        sI_token="c",
        eI_token="d",
        sO_token="e",
        eO_token="f",
        sR_token="g",
        eR_token="h",
        c0="i",
        c1="j",
        c2="k",
        c3="l",
        c4="m",
        c5="n",
        c6="o",
        c7="p",
        c8="q",
        c9="r",
    )

    encoded_pairs = grid_formatter.encode_pairs(task["train"])

    n_tokens = _estimate_n_tokens_per_pair(task)
    assert len(encoded_pairs) == sum(n_tokens[:-1])

    encoded_grid = grid_formatter.encode_grid(task["test"][0]["input"], "input")
    assert len(encoded_grid) == n_tokens[-1]
