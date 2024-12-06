import argparse
import logging

import polars as pl

from giotto_llm.consts import ROOT_PATH
from giotto_llm.generate_messages.messages_generator import MessagesGenerator
from giotto_llm.logs import get_named_logger
from giotto_llm.reader import ReaderPickle


def parse_arguments() -> dict:
    """Get the parameters required to start fine-tuning."""

    parser = argparse.ArgumentParser(description=f"Fine-tuning")

    parser.add_argument(
        "--output_file",
        type=str,
        required=True,
        help="Path to output file.",
    )

    parser.add_argument(
        "--path_to_tokenizer",
        type=str,
        required=True,
        help="Path to directory containing tokenizer configuration.",
    )

    parser.add_argument(
        "--dataset_category",
        type=str,
        required=True,
        help="Name of pickle containing training examples in ./synth_data/",
    )

    parser.add_argument(
        "--max_num_tasks_to_use",
        type=int,
        required=False,
        help="Use at most these many tasks to generate `Messages`, if not `None`.",
    )

    parser.add_argument(
        "--max_seq_length",
        type=int,
        required=True,
        help="Maximum number of tokens to allowed in the tokenized version of a `Messages` instance.",
    )

    parser.add_argument(
        "--num_messages_to_generate",
        type=int,
        required=True,
        help="Number of `Messages` instance to be generated.",
    )

    parser.add_argument(
        "--prompts_with_weights",
        type=str,
        required=True,
        help="Comma separated list of `prompt:weight` pairs, e.g. `prompt_solve_instr_v1:1,prompt_solve_instr_v2:2`",
    )

    parser.add_argument(
        "--transforms_with_weights",
        type=str,
        required=True,
        help="Comma separated list of `transforms:weight` pairs, e.g. `color_all_rigid_False:1,color_all_rigid_True:2`",
    )

    parser.add_argument(
        "--log_level",
        type=str,
        default="info",
        help="Logging level",
    )

    parser.add_argument(
        "--logger_name",
        type=str,
        default="finetuning",
        help="Logger name",
    )

    parser.add_argument(
        "--enable_log_to_file",
        action="store_true",
        help="Save runtime information in a log file",
    )

    arguments = parser.parse_args()

    # Validation
    assert arguments.log_level in {"debug", "info", "warning", "error", "critical"}

    map_log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    log_level = map_log_levels[arguments.log_level]
    logger = get_named_logger(
        name=f"{arguments.logger_name}_{arguments.dataset_category}",
        log_level=log_level,
        enable_log_to_file=arguments.enable_log_to_file,
        project_root=str(ROOT_PATH),
        output_dir="logs",
    )

    prompts_with_weights = {}
    if "," not in arguments.prompts_with_weights:
        prompt_type, weight = arguments.prompts_with_weights.split(":")
        prompts_with_weights[prompt_type] = int(weight)
    else:
        for prompt_type_weight in arguments.prompts_with_weights.split(","):
            prompt_type, weight = prompt_type_weight.split(":")
            prompts_with_weights[prompt_type] = int(weight)

    transforms_with_weights = {}
    if "," not in arguments.transforms_with_weights:
        transform_type, weight = arguments.transforms_with_weights.split(":")
        transforms_with_weights[transform_type] = int(weight)
    else:
        for transform_type_weight in arguments.transforms_with_weights.split(","):
            transform_type, weight = transform_type_weight.split(":")
            transforms_with_weights[transform_type] = int(weight)

    config = {
        "output_file": arguments.output_file,
        "path_to_tokenizer": arguments.path_to_tokenizer,
        "dataset_category": arguments.dataset_category,
        "max_num_tasks_to_use": arguments.max_num_tasks_to_use,
        "max_seq_length": arguments.max_seq_length,
        "num_messages_to_generate": arguments.num_messages_to_generate,
        "prompts_with_weights": prompts_with_weights,
        "transforms_with_weights": transforms_with_weights,
        "logger": logger,
    }
    return config


if __name__ == "__main__":
    config = parse_arguments()
    logger = config["logger"]

    logger.info(f">>> Reading tasks from {ROOT_PATH / 'synth_data' / config['dataset_category']}")
    reader = ReaderPickle(
        dataset_dir=str(ROOT_PATH / "synth_data"),
        dataset_category=config["dataset_category"],
        read_test_output=True,
    )
    _tasks = reader.read_tasks()
    tasks = {}

    if config["max_num_tasks_to_use"] is not None:
        logger.info(f">>> Filtering down to {config['max_num_tasks_to_use']} tasks")
        for idx, (task_id, task) in enumerate(_tasks.items()):
            tasks[task_id] = task
    else:
        tasks = _tasks

    messages_generator = MessagesGenerator(
        path_to_tokenizer=config["path_to_tokenizer"],
        max_seq_length=config["max_seq_length"],
        prompts_with_weights=config["prompts_with_weights"],
        transforms_with_weights=config["transforms_with_weights"],
        logger=config["logger"],
    )

    logger.info(f">>> Starting the generation of {config['num_messages_to_generate']} `Messages`")
    output = messages_generator(
        tasks=tasks,
        num_messages_to_generate=config["num_messages_to_generate"],
        random_seed=0,
    )
    df = pl.DataFrame(output)

    logger.info(f">>> Finished: {len(output)=}")
    logger.info(f">>> pl.DataFrame(output):\n{df}")
    df.write_parquet(
        config["output_file"],
        compression="zstd",
        compression_level=22,  # Note: maximum for zstd
    )
    logger.info(f">>> Written messages with metadata to {config['output_file']}")
