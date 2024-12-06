import os

import pytest

from giotto_llm.consts import ROOT_PATH
from giotto_llm.reader import ReaderMany, ReaderPickle
from giotto_llm.type_aliases import JSONTask


@pytest.mark.parametrize(
    "tasks", [{"dataset_type": "training"}, {"dataset_type": "evaluation"}], indirect=True
)
def test_read_tasks(tasks: dict[str, JSONTask]) -> None:

    assert isinstance(tasks, dict)
    for key, value in tasks.items():
        assert isinstance(key, str)
        assert isinstance(value, dict)

    assert len(tasks) == 400


@pytest.mark.parametrize(
    "dataset_dir, dataset_category",
    [
        ("synth_data", "ray-v5"),
    ],
)
def test_reader_pickle(dataset_dir: str, dataset_category: str) -> None:
    dataset_dir = f"{ROOT_PATH}/{dataset_dir}"
    assert os.path.exists(dataset_dir)

    reader = ReaderPickle(
        dataset_dir=dataset_dir,
        dataset_category=dataset_category,
    )
    tasks = reader.read_tasks()

    assert isinstance(tasks, dict)
    for key, value in tasks.items():
        assert isinstance(key, str)
        assert isinstance(value, dict)

    assert len(tasks) == 100_000
