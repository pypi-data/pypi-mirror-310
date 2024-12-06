"""Global fixtures"""

from typing import Any

import pytest
from _pytest.fixtures import FixtureRequest

from giotto_llm.causal_lm.models import CausalLMWrapper
from giotto_llm.consts import ROOT_PATH
from giotto_llm.reader import ReaderMany
from giotto_llm.type_aliases import JSONTask


@pytest.fixture(scope="session")
def tasks(request: FixtureRequest) -> dict[str, JSONTask]:
    dataset_dir = f"{ROOT_PATH}/kaggle/input"
    dataset_type = "training"
    read_test_output = True

    if hasattr(request, "param"):
        dataset_type = request.param.get("dataset_type", dataset_type)
        read_test_output = request.param.get("read_test_output", read_test_output)

    reader = ReaderMany(
        dataset_dir=dataset_dir,
        dataset_type=dataset_type,
        read_test_output=read_test_output,
    )
    return reader.read_tasks()


@pytest.fixture(scope="session")
def wrapper(request: FixtureRequest) -> CausalLMWrapper:
    model_id = str(ROOT_PATH / "models" / "llama" / "llama_3_2_1B_instruct")
    device = "cpu"
    if hasattr(request, "param"):
        device = request.param.get("device", device)

    if device == "cuda":
        config: dict[str, Any] = {"quantization_config": None, "device_map": {"": 0}}
    else:
        config = {"quantization_config": None, "device_map": "cpu", "low_cpu_mem_usage": True}
    wrapper = CausalLMWrapper(
        model_id=model_id,
        config=config,
    )
    return wrapper
