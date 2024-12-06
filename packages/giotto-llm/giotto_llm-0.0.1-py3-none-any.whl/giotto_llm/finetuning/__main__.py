import copy
import logging
import os
from functools import partial
from typing import Any, Literal

import mlflow
import numpy as np
import torch.distributed as dist
from huggingface_hub._login import _login as hf_login
from peft import LoraConfig
from sklearn.model_selection import ShuffleSplit
from torch.utils.data import Subset
from transformers import (
    EarlyStoppingCallback,
    TrainerCallback,
    TrainerControl,
    TrainerState,
    TrainingArguments,
)
from trl import SFTConfig, SFTTrainer

from giotto_llm.consts import ROOT_PATH
from giotto_llm.data import Dataset
from giotto_llm.finetuning.args import parse_arguments_main
from giotto_llm.finetuning.utils import MAP_WRAPPER, FinetuningConfig
from giotto_llm.prompts.consts import TYPES_OF_PROMPTS
from giotto_llm.prompts.grid_formatter import GridFormatter
from giotto_llm.reader import ReaderMany, ReaderPickle
from giotto_llm.transforms import Transforms, transform_task
from giotto_llm.utils import is_tf32_supported, split_tasks_by_test, write_json


class OnCheckpointCallback(TrainerCallback):
    def __init__(
        self, base_config: FinetuningConfig, *args: tuple[Any, ...], **kwargs: dict[Any, Any]
    ):
        super().__init__(*args, **kwargs)
        self.base_config = copy.deepcopy(base_config.dict())

    """Copy finetuning_config.json to the checkpoint dir, and modify paths"""

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs: dict[Any, Any],
    ) -> None:
        if not is_main_process():
            return
        output_dir = args.output_dir
        if os.path.isdir(args.output_dir):
            checkpoints = [
                d
                for d in os.listdir(output_dir)
                if d.startswith("checkpoint-") and os.path.isdir(os.path.join(args.output_dir, d))
            ]
            # Sort checkpoints by step number to get the latest one
            if checkpoints:
                latest_checkpoint = max(
                    checkpoints, key=lambda x: int(x.replace("checkpoint-", ""))
                )
                latest_checkpoint_path = os.path.join(args.output_dir, latest_checkpoint)
                self.base_config["output_dir"] = latest_checkpoint_path
                write_json(
                    data=self.base_config,
                    filename=f"{latest_checkpoint_path}/finetuning_config.json",
                )


def get_peft_config(
    target_modules: list[str] | str, dropout: float, alpha: int, r: int
) -> LoraConfig:
    """LoRA config based on QLoRA paper & Sebastian Raschka experiment"""
    return LoraConfig(
        lora_alpha=alpha,
        lora_dropout=dropout,
        r=r,
        bias="none",
        target_modules=target_modules,
        use_rslora=True,
        task_type="CAUSAL_LM",
    )


def get_sft_config(config: FinetuningConfig, log_mlflow: bool = True) -> SFTConfig:
    """Get the SFTConfig"""
    sft_config = SFTConfig(
        output_dir=config.output_dir,
        logging_dir=f"{config.output_dir}/logs",
        eval_strategy="epoch" if config.eval_steps is None else "steps",
        eval_steps=config.eval_steps,
        prediction_loss_only=True,
        per_device_train_batch_size=config.per_device_batch_size,
        per_device_eval_batch_size=config.per_device_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        max_seq_length=20_000,  # Not used for anything with custom collator
        eval_accumulation_steps=config.gradient_accumulation_steps,
        torch_empty_cache_steps=1 if config.low_memory is True else None,
        fp16_full_eval=config.low_memory,
        learning_rate=config.learning_rate,
        max_grad_norm=0.3,  # max gradient norm based on QLoRA paper
        num_train_epochs=config.num_train_epochs,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,  # warmup ratio based on QLoRA paper
        save_strategy="epoch" if config.eval_steps is None else "steps",
        save_steps=config.eval_steps,
        save_total_limit=config.save_total_limit,  # Can affect memory use
        save_only_model=True,
        seed=42,
        data_seed=42,
        fp16=not is_tf32_supported(),
        logging_strategy="epoch" if config.logging_steps is None else "steps",
        logging_steps=config.logging_steps,
        bf16=is_tf32_supported(),
        tf32=is_tf32_supported(),
        dataloader_num_workers=4,  # Should be sensible default
        remove_unused_columns=False,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        optim="adamw_torch_fused" if config.quantization == "no" else "adamw_8bit",
        report_to="mlflow" if log_mlflow is True else None,
        gradient_checkpointing=config.gradient_checkpointing or config.low_memory,
        neftune_noise_alpha=config.neftune_noise_alpha,
        use_liger_kernel=True,  # Still runs if not available
        gradient_checkpointing_kwargs={"use_reentrant": False},
        dataset_text_field="",  # need a dummy field for collator
        dataset_kwargs={"skip_prepare_dataset": True},  # important for collator
        dataloader_pin_memory=not config.low_memory,
    )
    sft_config.remove_unused_columns = False
    return sft_config


def get_train_eval_datasets(
    config: FinetuningConfig,
    model_type: Literal["image-text-to-text", "text-to-text"],
    grid_formatter: GridFormatter,
) -> tuple[Dataset | Subset, Dataset | Subset]:
    train_dataset = get_train_dataset(
        config=config, model_type=model_type, grid_formatter=grid_formatter
    )
    if config.eval_split_from_train is True:
        idx = np.arange(len(train_dataset))
        # This can fail based on user input, but it should be easy to understand what is wrong from the error
        train_idx, eval_idx = list(
            ShuffleSplit(
                n_splits=1,
                test_size=config.evaluation_set_size or 0.2,
                train_size=config.training_set_size,
            ).split(idx)
        )[0]
        train_subset: Dataset | Subset = Subset(train_dataset, train_idx)
        eval_dataset: Dataset | Subset = Subset(train_dataset, eval_idx)
    else:
        if config.training_set_size is None or config.training_set_size >= len(train_dataset):
            train_subset = train_dataset
        else:
            idx = np.arange(len(train_dataset))
            train_idx = list(
                ShuffleSplit(n_splits=1, test_size=None, train_size=config.training_set_size).split(
                    idx
                )
            )[0][0]
            train_subset = Subset(train_dataset, train_idx)

        eval_dataset = get_eval_dataset(
            config=config,
            model_type=model_type,
            size=config.evaluation_set_size or len(train_dataset) // 5,
            grid_formatter=grid_formatter,
        )
    return train_subset, eval_dataset


def get_train_dataset(
    config: FinetuningConfig,
    model_type: Literal["image-text-to-text", "text-to-text"],
    grid_formatter: GridFormatter,
) -> Dataset:
    tasks = ReaderPickle(dataset_dir="./synth_data", dataset_category=config.dataset).read_tasks()
    tasks = split_tasks_by_test(tasks)

    transforms = Transforms(
        test=True,
        order="reorder",
        color="all" if config.transform_background_color is True else "foreground",
        limit_colors=config.compress_colors,
        rigid=True,
    )
    dataset: Dataset = Dataset(
        tasks=tasks,
        transforms=transforms,
        messages_fn=TYPES_OF_PROMPTS[config.prompt_type](grid_formatter=grid_formatter),
        model_type=model_type,
    )
    return dataset


def get_eval_dataset(
    config: FinetuningConfig,
    model_type: Literal["image-text-to-text", "text-to-text"],
    size: int,
    grid_formatter: GridFormatter,
) -> Dataset:
    tasks = ReaderMany(
        dataset_dir=f"{ROOT_PATH}/kaggle/input",
        dataset_type="evaluation",
        read_test_output=True,
    ).read_tasks()
    size = size if config.evaluation_set_size is None else config.evaluation_set_size

    tasks = split_tasks_by_test(tasks)
    if len(tasks) > size:
        tasks = {key: value for i, (key, value) in enumerate(tasks.items()) if i < size}

    # Augment tasks with random transforms until reaching the requested size
    augmented_tasks = copy.deepcopy(tasks)
    np.random.seed(42)
    transforms = Transforms(
        test=True,
        order="reorder",
        color="all" if config.transform_background_color is True else "foreground",
        limit_colors=False,
        rigid=True,
    )
    iteration = 0
    current_size = len(tasks)
    while True:
        for task_id, task in tasks.items():
            if current_size >= size:
                break
            augmented_tasks[f"{task_id}-{iteration}"] = transform_task(
                task=task, transforms=transforms
            )[0]
            current_size += 1
        else:
            iteration += 1
            continue
        break

    transforms = Transforms(
        test=False,
        order=None,
        color=None,
        limit_colors=config.compress_colors,
        rigid=False,
    )
    dataset = Dataset(
        tasks=augmented_tasks,
        transforms=transforms,
        messages_fn=TYPES_OF_PROMPTS[config.prompt_type](grid_formatter=grid_formatter),
        model_type=model_type,
    )
    return dataset


def main(logger: logging.Logger, config: FinetuningConfig) -> None:
    """Finetune model"""
    if not os.path.exists(config.output_dir):
        os.mkdir(config.output_dir)
    write_json(data=config.dict(), filename=f"{config.output_dir}/finetuning_config.json")

    wrapper_cls = MAP_WRAPPER[config.wrapper]

    logger.info("Initializing model")
    wrapper = wrapper_cls(model_id=config.model_id, quantization=config.quantization)

    if config.untie_word_embeddings is True:
        wrapper.untie_word_embeddings()

    peft_config = get_peft_config(
        target_modules=(
            wrapper._target_modules
            if config.lora_target_modules is None
            else config.lora_target_modules
        ),
        dropout=config.lora_dropout,
        alpha=config.lora_alpha,
        r=config.lora_r,
    )
    sft_config = get_sft_config(config=config, log_mlflow=True)

    logger.info("Creating datasets")
    train_dataset, eval_dataset = get_train_eval_datasets(
        config=config,
        model_type=wrapper.model_type,
        grid_formatter=wrapper.grid_formatter,
    )
    if is_main_process():
        print(f">>> {train_dataset[0][0]=}")

    if config.padding_side is not None:
        wrapper.tokenizer.padding_side = config.padding_side

    callbacks = [
        EarlyStoppingCallback(early_stopping_patience=config.early_stopping_patience),
        OnCheckpointCallback(base_config=config),
    ]

    if is_main_process():
        mlflow.set_tag("mlflow.runName", config.output_dir)
        mlflow.log_params(
            config.dict() | {"train_size": len(train_dataset), "eval_size": len(eval_dataset)}
        )

    trainer = SFTTrainer(
        model=wrapper.model,
        args=sft_config,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=partial(wrapper.collate_fn_train, mask_inputs=not config.disable_input_mask),
        peft_config=peft_config,
        callbacks=callbacks,
    )
    logger.info("Training model")
    if dist.is_available() and dist.is_initialized():
        dist.barrier()
    trainer.train()
    # Sync processes
    if dist.is_available() and dist.is_initialized():
        dist.barrier()
    if is_main_process():
        logger.info("Saving model")
        trainer.model.to("cpu")
        trainer.save_model(config.output_dir)
        logger.info(f"Saving {wrapper.grid_formatter=}")
        wrapper.grid_formatter.save(config.output_dir)


def is_main_process() -> bool:
    return "RANK" not in os.environ or int(os.environ["RANK"]) == 0


if __name__ == "__main__":
    if "HF_TOKEN" in os.environ:
        HF_TOKEN = os.environ["HF_TOKEN"]
        hf_login(token=HF_TOKEN, add_to_git_credential=False)
    args = parse_arguments_main()
    config = FinetuningConfig(
        model_id=args["model_id"],
        wrapper=args["wrapper"],
        output_dir=args["output_dir"],
        quantization=args["quantization"],
        dataset=args["dataset"],
        transform_background_color=args["transform_background_color"],
        compress_colors=args["compress_colors"],
        learning_rate=args["learning_rate"],
        per_device_batch_size=args["batch_size"],
        gradient_accumulation_steps=args["gradient_accumulation_steps"],
        num_train_epochs=args["num_train_epochs"],
        neftune_noise_alpha=args["neftune_noise_alpha"],
        padding_side=args["padding_side"],
        prompt_type=args["prompt_type"],
        lora_target_modules=args["lora_target_modules"],
        training_set_size=args["training_set_size"],
        evaluation_set_size=args["evaluation_set_size"],
        logging_steps=args["logging_steps"],
        eval_steps=args["eval_steps"],
        low_memory=args["low_memory"],
        lora_dropout=args["lora_dropout"],
        lora_alpha=args["lora_alpha"],
        lora_r=args["lora_r"],
        early_stopping_patience=args["early_stopping_patience"],
        save_total_limit=args["save_total_limit"],
        untie_word_embeddings=args["untie_word_embeddings"],
        eval_split_from_train=args["eval_split_from_train"],
        disable_input_mask=args["disable_input_mask"],
        gradient_checkpointing=args["gradient_checkpointing"],
    )
    main(logger=args["logger"], config=config)
