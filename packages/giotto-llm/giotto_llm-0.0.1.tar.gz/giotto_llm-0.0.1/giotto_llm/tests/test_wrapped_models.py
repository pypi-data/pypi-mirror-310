from giotto_llm.causal_lm.models import CausalLMWrapper
from giotto_llm.consts import DEFAULT_END_EXAMPLE_TOKEN, DEFAULT_START_EXAMPLE_TOKEN, ROOT_PATH


def test_init_causal_lm_wrapper(wrapper: CausalLMWrapper) -> None:
    assert wrapper.grid_formatter.sE_token == DEFAULT_START_EXAMPLE_TOKEN
    assert wrapper.grid_formatter.eE_token == DEFAULT_END_EXAMPLE_TOKEN
