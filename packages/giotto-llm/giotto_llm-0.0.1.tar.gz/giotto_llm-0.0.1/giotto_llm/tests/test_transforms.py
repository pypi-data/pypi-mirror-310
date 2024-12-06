import pytest

from giotto_llm.consts import ROOT_PATH
from giotto_llm.reader import ReaderMany
from giotto_llm.transforms import Transforms, backtransform_test_output, transform_task
from giotto_llm.type_aliases import JSONTask
from giotto_llm.utils import split_tasks_by_test


@pytest.mark.parametrize("tasks", [{"read_test_output": False}], indirect=True)
@pytest.mark.parametrize(
    "transforms",
    [
        Transforms(color="all"),
        Transforms(color="foreground"),
        Transforms(limit_colors=True),
        Transforms(rigid=True),
        Transforms(color="all", limit_colors=True, rigid=True),
    ],
)
def test_transforms(tasks: dict[str, JSONTask], transforms: Transforms) -> None:
    """Test that the transforms succeeds without test output"""
    tasks = split_tasks_by_test(tasks)
    for task in tasks.values():
        assert "output" not in task["test"][0]
        transform_task(task=task, transforms=transforms)


@pytest.mark.parametrize(
    "transforms",
    [
        Transforms(color="all"),
        Transforms(color="foreground"),
        Transforms(limit_colors=True),
        Transforms(rigid=True),
        Transforms(color="all", limit_colors=True, rigid=True),
    ],
)
def test_backtransforms(tasks: dict[str, JSONTask], transforms: Transforms) -> None:
    tasks = split_tasks_by_test(tasks)
    for task in tasks.values():
        transformed_task, backtransform = transform_task(task=task, transforms=transforms)
        backtransformed_output = backtransform_test_output(
            grid=transformed_task["test"][0]["output"], backtransform=backtransform
        )
        assert str(backtransformed_output) == str(task["test"][0]["output"])


@pytest.mark.parametrize(
    "max_tokens,train_pairs",
    [(None, 5), (100_000, 5), (280, 4), (230, 3), (180, 2), (130, 1), (0, 1)],
)
def test_max_tokens(max_tokens: int | None, train_pairs: int, tasks: dict[str, JSONTask]) -> None:
    """Test that the size is as expected"""
    task_id = "fafffa47"
    task = tasks[task_id]

    transform = Transforms(max_tokens=max_tokens)
    transformed_task = transform_task(task, transform)[0]
    assert len(transformed_task["train"]) == train_pairs
