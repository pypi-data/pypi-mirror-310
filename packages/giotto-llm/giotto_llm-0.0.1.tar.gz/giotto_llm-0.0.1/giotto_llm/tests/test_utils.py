import pytest

from giotto_llm.utils import RepeatSampler


def test_repeat_sampler() -> None:
    sequence = list(RepeatSampler(n_repeats=2, size=3))
    assert sequence == [0, 0, 1, 1, 2, 2]
