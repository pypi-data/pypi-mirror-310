import os
import pathlib

from peft import PeftModel

from .args import parse_arguments_merge
from .utils import MAP_WRAPPER, FinetuningConfig


def merge_model(config: FinetuningConfig, adaptor_path: str, merge_path: str) -> None:
    base_model_id = pathlib.Path(config.model_id).resolve(strict=True)
    assert base_model_id.exists(), f"{base_model_id=} does not exist"

    print(f">>> Loading {base_model_id}")
    wrapper_cls = MAP_WRAPPER[config.wrapper]
    wrapper = wrapper_cls(
        model_id=str(base_model_id),
        config={
            "quantization_config": None,
            "device_map": "cpu",
            "low_cpu_mem_usage": True,
        },
    )
    print(f">>> {wrapper=}")

    if config.padding_side is not None:
        wrapper.tokenizer.padding_side = config.padding_side

    if config.untie_word_embeddings:
        wrapper.untie_word_embeddings()

    print(f">>> Creating merged model from {base_model_id} and {adaptor_path=} in {merge_path=}")
    wrapper.model = PeftModel.from_pretrained(
        wrapper.model,
        adaptor_path,
        safe_serialization=True,
        max_shard_size="2GB",
        trust_remote_code=False,
    ).merge_and_unload()
    wrapper.data_config = {
        "compress_colors": config.compress_colors,
        "transform_background_color": config.transform_background_color,
        "prompt_type": config.prompt_type,
    }
    wrapper.save_pretrained(merge_path)


def load_finetuning_config(adaptor_path: str) -> FinetuningConfig:
    config_path = adaptor_path + "/finetuning_config.json"
    if "checkpoint" in config_path and not os.path.exists(config_path):
        base_path = pathlib.Path(adaptor_path).parent
        config_path = str(base_path / "finetuning_config.json")
        finetuning_config = FinetuningConfig.parse_file(config_path)
        finetuning_config.output_dir = adaptor_path
    else:
        finetuning_config = FinetuningConfig.parse_file(config_path)
    return finetuning_config


if __name__ == "__main__":
    args = parse_arguments_merge()
    config = load_finetuning_config(args["adaptor_path"])

    merge_model(config, args["adaptor_path"], args["merge_path"])
