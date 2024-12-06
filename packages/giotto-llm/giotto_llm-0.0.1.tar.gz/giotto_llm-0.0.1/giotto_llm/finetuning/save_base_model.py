import argparse

from giotto_llm.finetuning.utils import MAP_WRAPPER


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, required=True)
    parser.add_argument("--wrapper", type=str, required=True)
    parser.add_argument("--output_model_dir", type=str, required=True)
    args = parser.parse_args()

    return {
        "model_id": args.model_id,
        "wrapper": args.wrapper,
        "output_model_dir": args.output_model_dir,
    }


if __name__ == "__main__":
    arguments = parse_arguments()
    model_id = arguments["model_id"]
    wrapper = arguments["wrapper"]
    output_model_dir = arguments["output_model_dir"]

    wrapper_cls = MAP_WRAPPER[wrapper]
    wrapper = wrapper_cls(
        model_id=model_id,
        config={"quantization_config": None, "device_map": "cpu", "low_cpu_mem_usage": True},
    )
    print(f">>> Loaded wrapped model with dtype={wrapper.model.dtype}")

    wrapper.save_pretrained(output_model_dir)
