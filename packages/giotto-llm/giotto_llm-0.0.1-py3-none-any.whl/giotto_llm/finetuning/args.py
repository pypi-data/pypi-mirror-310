import argparse
import logging
from typing import Any, Literal

from ..consts import ROOT_PATH
from ..logs import get_named_logger

map_log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def parse_arguments_main() -> dict[str, Any]:
    """Get the parameters required to start fine-tuning."""

    parser = argparse.ArgumentParser(description=f"Fine-tuning")

    parser.add_argument(
        "-d",
        "--dataset",
        type=str,
        required=True,
        help="Location of training examples. Will look for a matching pickle in ./synth_data/, or a matching table name in BigQuery.",
    )

    parser.add_argument(
        "--model_id",
        type=str,
        required=True,
        help="Huggingface base-model id.",
    )

    parser.add_argument(
        "--wrapper",
        type=str,
        required=True,
        help="Which wrapper to use for the model.",
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        required=True,
        help="Output dir to save model to.",
    )

    parser.add_argument(
        "--quantization",
        type=str,
        default=None,
        help="Which quantization setting to use,",
    )

    parser.add_argument(
        "--transform_background_color",
        action="store_true",
        help="Whether or not to transform background color in the dataloader,",
    )

    parser.add_argument(
        "--compress_colors",
        action="store_true",
        help="Whether or not to do color compression in the dataloader,",
    )

    parser.add_argument(
        "--learning_rate",
        type=float,
        default=3e-4,
        help="The initial learning rate.",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="The batch size on each device.",
    )

    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=4,
        help="The number of gradient accumulation steps.",
    )

    parser.add_argument(
        "--num_train_epochs",
        type=int,
        default=5,
        help="The number of training epochs",
    )

    parser.add_argument(
        "--neftune_noise_alpha",
        type=float,
        default=None,
        help="The amount of noise to add embeddings",
    )

    parser.add_argument(
        "--padding_side",
        type=str,
        default=None,
        help="Override default padding side ('left' or 'right')",
    )

    parser.add_argument(
        "--prompt_type",
        type=str,
        default="prompt_solve_short",
        help="The type of text prompt to use",
    )

    parser.add_argument(
        "--training_set_size",
        type=int,
        default=None,
        help="The training set size. If not specified, use the full dataset.",
    )

    parser.add_argument(
        "--evaluation_set_size",
        type=int,
        default=None,
        help="The evaluation set size. If not specified, use 20% of the training set.",
    )

    parser.add_argument(
        "--lora_target_modules",
        type=str,
        default=None,
        nargs="+",
        help="The target modules for Lora. If not specified, target all linear layers.",
    )

    parser.add_argument(
        "--logging_steps",
        type=str,
        default=None,
        help="Number of steps between each log entry. If not specified, log per epoch.",
    )

    parser.add_argument(
        "--eval_steps",
        type=str,
        default=None,
        help="Number of steps between each pass of the evaluation set. If not specified, evaluate once per epoch.",
    )

    parser.add_argument(
        "--low_memory",
        action="store_true",
        help="Enable options that save memory at the expense of performance.",
    )

    parser.add_argument(
        "--lora_dropout",
        type=float,
        default=0.2,
        help="The dropout used in Lora.",
    )

    parser.add_argument(
        "--lora_alpha",
        type=int,
        default=16,
        help="The alpha used in Lora.",
    )
    parser.add_argument(
        "--lora_r",
        type=int,
        default=8,
        help="The r used in Lora.",
    )

    parser.add_argument(
        "--early_stopping_patience",
        type=int,
        default=3,
        help="The early stopping patience.",
    )

    parser.add_argument(
        "--save_total_limit",
        type=int,
        default=None,
        help="How many checkpoints to keep.",
    )

    parser.add_argument(
        "--untie_word_embeddings",
        action="store_true",
        help="Untie the word embeddings from the classification head.",
    )

    parser.add_argument(
        "--eval_split_from_train",
        action="store_true",
        help="Use a random subset of the training set for evaluation instead of the kaggle eval set.",
    )

    parser.add_argument(
        "--disable_input_mask",
        action="store_true",
        help="Disable masking of the model inputs.",
    )

    parser.add_argument(
        "--gradient_checkpointing",
        action="store_true",
        help="Use gradient checkpointing",
    )

    parser.add_argument(
        "-l",
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

    log_level = map_log_levels[arguments.log_level]
    logger = get_named_logger(
        name=f"{arguments.logger_name}_{arguments.dataset}",
        log_level=log_level,
        enable_log_to_file=arguments.enable_log_to_file,
        project_root=str(ROOT_PATH),
        output_dir="logs",
    )

    return {
        "logger": logger,
        "dataset": arguments.dataset,
        "model_id": arguments.model_id,
        "wrapper": arguments.wrapper,
        "output_dir": arguments.output_dir,
        "quantization": arguments.quantization,
        "transform_background_color": arguments.transform_background_color,
        "compress_colors": arguments.compress_colors,
        "learning_rate": arguments.learning_rate,
        "batch_size": arguments.batch_size,
        "gradient_accumulation_steps": arguments.gradient_accumulation_steps,
        "num_train_epochs": arguments.num_train_epochs,
        "neftune_noise_alpha": arguments.neftune_noise_alpha,
        "padding_side": arguments.padding_side,
        "prompt_type": arguments.prompt_type,
        "lora_target_modules": arguments.lora_target_modules,
        "training_set_size": arguments.training_set_size,
        "evaluation_set_size": arguments.evaluation_set_size,
        "logging_steps": arguments.logging_steps,
        "eval_steps": arguments.eval_steps,
        "low_memory": arguments.low_memory,
        "lora_dropout": arguments.lora_dropout,
        "lora_alpha": arguments.lora_alpha,
        "lora_r": arguments.lora_r,
        "early_stopping_patience": arguments.early_stopping_patience,
        "save_total_limit": arguments.save_total_limit,
        "untie_word_embeddings": arguments.untie_word_embeddings,
        "eval_split_from_train": arguments.eval_split_from_train,
        "disable_input_mask": arguments.disable_input_mask,
        "gradient_checkpointing": arguments.gradient_checkpointing,
    }


def parse_arguments_merge() -> dict[str, str]:
    """Get the parameters required to merge base-model and adaptor."""

    parser = argparse.ArgumentParser(description=f"Merge")

    parser.add_argument(
        "--adaptor_path",
        type=str,
        required=True,
        help="The path to the adaptor (or checkpoint)",
    )

    parser.add_argument(
        "--merge_path",
        type=str,
        required=True,
        help="The path to the merged model",
    )

    arguments = parser.parse_args()

    return {
        "adaptor_path": arguments.adaptor_path,
        "merge_path": arguments.merge_path,
    }


def parse_arguments_prune() -> dict[str, str | float]:
    """Get the parameters required to merge base-model and adaptor."""

    parser = argparse.ArgumentParser(description=f"Merge")

    parser.add_argument(
        "--model_id",
        type=str,
        required=True,
        help="The base model id (path)",
    )

    parser.add_argument(
        "--wrapper",
        type=str,
        required=True,
        help="Which wrapper to use for the model.",
    )

    parser.add_argument(
        "--prune_path",
        type=str,
        required=True,
        help="The path to save the pruned model",
    )

    parser.add_argument(
        "--prune_ratio",
        type=float,
        default=0.5,
        help="The pruning ratio.",
    )

    parser.add_argument(
        "--prune_steps",
        type=int,
        default=1,
        help="The number of iterative pruning steps.",
    )

    parser.add_argument(
        "--global_pruning",
        action="store_true",
        help="Enable global pruning.",
    )

    arguments = parser.parse_args()

    return {
        "model_id": arguments.model_id,
        "wrapper": arguments.wrapper,
        "prune_path": arguments.prune_path,
        "prune_ratio": arguments.prune_ratio,
        "global_pruning": arguments.global_pruning,
        "prune_steps": arguments.prune_steps,
    }
