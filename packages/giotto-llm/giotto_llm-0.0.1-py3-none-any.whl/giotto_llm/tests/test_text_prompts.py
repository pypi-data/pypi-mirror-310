from pathlib import Path

import pytest
from transformers import AutoTokenizer

from giotto_llm.consts import (
    C1,
    C2,
    C3,
    C4,
    DEFAULT_END_OUTPUT_TOKEN,
    DEFAULT_END_ROW_TOKEN,
    DEFAULT_START_OUTPUT_TOKEN,
    DEFAULT_START_ROW_TOKEN,
)
from giotto_llm.prompts.grid_formatter import GridFormatter
from giotto_llm.prompts.text_prompts import PromptSolveInstrV1, PromptSolveInstrV2, TextPromptBase
from giotto_llm.type_aliases import JSONTask

path_to_llama_tokenizer = Path(__file__).parent / "llama_tokenizer"
llama_tokenizer = AutoTokenizer.from_pretrained(
    path_to_llama_tokenizer,
    trust_remote_code=False,
)


@pytest.mark.parametrize(
    "task, formatted_test_0_output, prompt_fn",
    [
        (
            {
                "train": [{"input": [[0, 0], [0, 0]], "output": [[1, 2], [3, 4]]}],
                "test": [{"input": [[0, 0], [0, 0]], "output": [[1, 2], [3, 4]]}],
            },
            (
                f"{DEFAULT_START_OUTPUT_TOKEN}"
                f"{DEFAULT_START_ROW_TOKEN}{C1}{C2}{DEFAULT_END_ROW_TOKEN}"
                f"{DEFAULT_START_ROW_TOKEN}{C3}{C4}{DEFAULT_END_ROW_TOKEN}"
                f"{DEFAULT_END_OUTPUT_TOKEN}"
            ),
            PromptSolveInstrV1(grid_formatter=GridFormatter()),
        ),
        (
            {
                "train": [{"input": [[0, 0], [0, 0]], "output": [[1, 2], [3, 4]]}],
                "test": [{"input": [[0, 0], [0, 0]], "output": [[1, 2], [3, 4]]}],
            },
            (
                f"{DEFAULT_START_OUTPUT_TOKEN}"
                f"{DEFAULT_START_ROW_TOKEN}{C1}{C2}<|other_end_token|>"
                f"{DEFAULT_START_ROW_TOKEN}{C3}{C4}<|other_end_token|>"
                f"{DEFAULT_END_OUTPUT_TOKEN}"
            ),
            PromptSolveInstrV2(grid_formatter=GridFormatter(eR_token="<|other_end_token|>")),
        ),
    ],
)
def test_prompt_solve_v1(
    task: JSONTask, formatted_test_0_output: str, prompt_fn: TextPromptBase
) -> None:
    formatted_grid = prompt_fn.generate_assistant(task=task, idx_i=0)

    print(f"D: {prompt_fn(task=task, idx_i=0)}")
    assert formatted_test_0_output == formatted_grid
