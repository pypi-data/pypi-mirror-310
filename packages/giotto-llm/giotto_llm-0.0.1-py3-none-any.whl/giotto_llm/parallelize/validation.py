import copy
import glob
import json
import logging
import os
import subprocess
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
from easydict import EasyDict

from giotto_llm.consts import ROOT_PATH
from giotto_llm.logs import get_named_logger
from giotto_llm.reader import ReaderMany
from giotto_llm.validation.args import parse_arguments
from giotto_llm.validation.monitor import log_resource_usage

TIME_LIMIT = 1_000_000
MAX_CPU_TIME_PER_TASK_S = 40 * 60  # 40 minutes per CPU task
MAX_CPU_EXECUTION_TIME = 2 * 60 * 60  # 2 h

process_counter = 0


def process_batch(
    arguments: EasyDict,
    model_name: str,
    batch_start: int,
    batch_end: int,
    gpu_index: int,
    logs_dir_path: str,
    logger: logging.Logger,
) -> tuple[subprocess.Popen, int]:
    """
    Start a new process on the gpu_index on tasks from batch_start to batch_end (indices).
    """
    global process_counter

    cmd = assemble_commmand_from_arguments(
        arguments=arguments,
        gpu_index=gpu_index,
        start_index_tasks=batch_start,
        end_index_tasks=batch_end,
    )
    if arguments.cpu_only:
        log_file_gpu = os.path.join(str(logs_dir_path), f"output_validation_{model_name}_cpu.log")
    else:
        log_file_gpu = os.path.join(
            str(logs_dir_path), f"output_validation_{model_name}_gpu_{gpu_index}.log"
        )
    logger.info(f">>> Going to run the following command as subprocess")
    logger.info(f"\t- {cmd}")
    with open(log_file_gpu, "a") as f:
        f.write(f"Processing tasks from {batch_start} to {batch_end} on GPU {gpu_index}")
        process_counter += 1
        pro = subprocess.Popen(
            cmd,
            shell=False,
            start_new_session=True,
            stdout=f,
            stderr=f,
        )
    process_id = process_counter
    return pro, process_id


def main(
    arguments: EasyDict,
    logger: logging.Logger,
) -> None:
    # --------------------------------------------------------------------
    # Setup folders and files
    # --------------------------------------------------------------------
    model_name = Path(arguments.finetuned_model_id).parts[-1]
    today = datetime.now()
    date_string = today.strftime("%Y_%m_%d")
    submission_dir_path = str(ROOT_PATH / "subs" / date_string)
    os.makedirs(str(submission_dir_path), exist_ok=True)
    logs_dir_path = str(ROOT_PATH / "logs" / date_string)
    os.makedirs(str(logs_dir_path), exist_ok=True)

    total_start_time = time.time()
    logger.info(f">>> Starting parallelized validation")
    logger.info(f">>> Saving submission.json files to {submission_dir_path}")
    logger.info(f">>> Saving logs to {logs_dir_path}")
    logger.info("-" * 30)

    number_gpus = count_available_gpus()
    logger.info(f">>> Found {number_gpus} GPUs")

    # --------------------------------------------------------------------
    # Read tasks
    # --------------------------------------------------------------------
    tasks = ReaderMany(
        dataset_dir=arguments.dataset_dir,
        dataset_type=arguments.dataset_type,
        read_test_output=False,
    ).read_tasks()
    tasks_ids: list[str] = sorted(tasks)
    tasks_ids = tasks_ids[arguments.start_index_tasks : arguments.end_index_tasks]
    total_num_tasks = len(tasks_ids)
    logger.info(
        f">>> Found {total_num_tasks} tasks with {arguments.dataset_dir=}, {arguments.dataset_type=}"
    )

    # --------------------------------------------------------------------
    # Divide tasks in batches
    # --------------------------------------------------------------------
    batch_size = (
        int(arguments.num_tasks_per_gpu_process)
        if arguments.num_tasks_per_gpu_process > 0
        else total_num_tasks // number_gpus
    )
    total_batches = np.ceil(total_num_tasks / batch_size).astype("int")
    logger.info(
        f">>> Dividing tasks into {total_batches} batches, each with up to {batch_size} tasks"
    )

    def get_batch_start_end_idxs(batch_id: int) -> tuple[int, int]:
        assert batch_id < total_batches, f"{batch_id=} is greater than {total_batches=}"
        start_idx = arguments.start_index_tasks + batch_size * batch_id
        end_idx = min(start_idx + batch_size, arguments.end_index_tasks)
        return start_idx, end_idx

    available_gpus = deque(range(number_gpus))
    remaining_batches = deque(range(total_batches))
    active_processes: dict[int, tuple[subprocess.Popen, int, int]] = (
        {}
    )  # Dictionary to keep track of active child processes and their assigned batches and gpu index

    # --------------------------------------------------------------------
    # Start processes
    # --------------------------------------------------------------------
    while available_gpus:
        gpu_idx = available_gpus.popleft()  # Get next available GPU
        if remaining_batches:
            next_batch = remaining_batches.popleft()  # Get next available batch
            start_idx, end_idx = get_batch_start_end_idxs(next_batch)
            pro, pro_id = process_batch(
                arguments, model_name, start_idx, end_idx, gpu_idx, logs_dir_path, logger
            )  # Start child process
            active_processes[pro_id] = (pro, next_batch, gpu_idx)

    logger.info(f">>> Started subprocesses: {active_processes}")
    time.sleep(20)

    # --------------------------------------------------------------------
    # Relaunch processes until all tasks have been analyzed
    # --------------------------------------------------------------------
    finished_batches: list[int] = []
    failed_batches: list[int] = []
    finished_task_ids: list[str] = []
    failed_task_ids: list[str] = []
    while active_processes:
        finished_processes: list[int] = []
        for pro_id, (pro, batch_id, gpu_idx) in list(active_processes.items()):
            if pro.poll() is not None:  # Process finished
                finished_processes.append(pro_id)
                available_gpus.append(gpu_idx)  # Release GPU
                start_idx, end_idx = get_batch_start_end_idxs(batch_id)

                if pro.returncode == 0:  # Process finished successfully
                    finished_batches.append(batch_id)
                    successful_tasks = tasks_ids[start_idx:end_idx]
                    finished_task_ids += successful_tasks
                    logger.info(
                        f">>> Task batch {batch_id} successful, with tasks {successful_tasks}"
                    )
                else:  # Process failed
                    failed_batches.append(batch_id)
                    failed_tasks = tasks_ids[start_idx:end_idx]
                    failed_task_ids += failed_tasks
                    logger.warning(f">>> Task batch {batch_id} failed, with tasks {failed_tasks}")

                if remaining_batches:
                    next_batch = remaining_batches.popleft()  # Get next available batch
                    start_idx, end_idx = get_batch_start_end_idxs(next_batch)
                    pro, pro_id = process_batch(
                        arguments, model_name, start_idx, end_idx, gpu_idx, logs_dir_path, logger
                    )  # Start child process
                    active_processes[pro_id] = (pro, next_batch, gpu_idx)
                    time.sleep(20)

        for pro_id in finished_processes:
            del active_processes[pro_id]

    # --------------------------------------------------------------------
    #       Retry taskes on CPU
    # --------------------------------------------------------------------
    logger.info(f">>> Retrying {failed_batches} batches with CPU")
    failed_batches_copy = copy.deepcopy(failed_batches)
    cpu_start_time = time.time()
    for batch_id in failed_batches_copy:
        if time.time() - cpu_start_time > MAX_CPU_EXECUTION_TIME:
            logger.warning(
                f"Exceeded maximum CPU execution time of {MAX_CPU_EXECUTION_TIME/3600.0:.2f}. Exiting retry loop."
            )
            break

        start = time.time()
        start_idx, end_idx = get_batch_start_end_idxs(batch_id)
        arguments.cpu_only = True
        pro, pro_id = process_batch(
            arguments, model_name, start_idx, end_idx, 0, logs_dir_path, logger
        )

        # Wait for process to finish or for timeout
        while pro.poll() is None:
            time.sleep(10)
            if time.time() - start > MAX_CPU_TIME_PER_TASK_S:
                pro.terminate()
                pro.wait()
                break

        if pro.returncode == 0:
            finished_batches.append(batch_id)
            failed_batches.remove(batch_id)
            successful_tasks = tasks_ids[start_idx:end_idx]
            finished_task_ids += successful_tasks
            logger.info(f">>> Task batch {batch_id} successful, with tasks {successful_tasks}")
        else:
            failed_tasks = tasks_ids[start_idx:end_idx]
            failed_task_ids += failed_tasks
            logger.warning(f">>> Task batch {batch_id} failed, with tasks {failed_tasks}")

    # --------------------------------------------------------------------
    # Merge submission files
    # --------------------------------------------------------------------
    total_end_time = time.time()
    logger.info(f">>> Finished after {total_end_time - total_start_time:.2f} seconds")
    logger.info(f">>> Successful batches: {finished_batches}")
    logger.info(f">>> Failed batches: {failed_batches}")
    logger.info(f">>> Tasks with predictions: {finished_task_ids}")
    logger.info(f">>> Tasks without prediction: {failed_task_ids}")

    # Save a single submission.json
    submission_file_path = os.path.join(
        submission_dir_path,
        f"submission_{model_name}_*.json",
    )
    final_submission_file_path = os.path.join(
        submission_dir_path,
        f"submission_{model_name}.json",
    )
    submission_files = glob.glob(submission_file_path)
    logger.info(f">>> Found {submission_files}")

    final_sub = dict()
    for sub_file in submission_files:
        with open(sub_file, "r") as f:
            subset_sub = json.load(f)
            final_sub.update(copy.deepcopy(subset_sub))

    logger.info(f">>> Writing final submission file")
    with open(final_submission_file_path, "w") as output_file:
        json.dump(final_sub, output_file)


def count_available_gpus() -> int:
    """Return the number of GPUs in this node"""
    if not torch.cuda.is_available():
        raise SystemError("No GPU device is available to torch")

    return torch.cuda.device_count()


def assemble_commmand_from_arguments(
    arguments: EasyDict,
    gpu_index: int,
    start_index_tasks: int,
    end_index_tasks: int,
) -> list[str]:
    """Assemble a command to be run as a subproces that will use exactly one GPU."""

    cmd_list = [
        "python",
        "-m",
        "giotto_llm.validation",
        "--finetuned_model_id",
        str(arguments.finetuned_model_id),
        "--dataset_dir",
        str(arguments.dataset_dir),
        "--dataset_type",
        str(arguments.dataset_type),
        "--image_resize_factor",
        str(arguments.image_resize_factor),
        "--n_dataloader_workers",
        str(arguments.n_dataloader_workers),
        "--batch_size",
        str(arguments.batch_size),
        "--wrapper_cls_type",
        str(arguments.wrapper_cls_type),
        "--quantization",
        str(arguments.quantization),
        "--n_attempts",
        str(arguments.n_attempts),
        "--n_transforms",
        str(arguments.n_transforms),
        "--max_new_tokens",
        str(arguments.max_new_tokens),
        "--num_return_sequences",
        str(arguments.num_return_sequences),
        "--num_beams",
        str(arguments.num_beams),
        "--start_index_tasks",
        str(int(start_index_tasks)),
        "--end_index_tasks",
        str(int(end_index_tasks)),
        "--gpu_index",
        str(gpu_index),
        "--random_seed",
        str(arguments.random_seed),
        "--input_tokens_limit",
        str(arguments.input_tokens_limit),
    ]

    if arguments.cpu_only:
        cmd_list.append("--cpu_only")

    if arguments.save_generation_metadata:
        cmd_list.append("--save_generation_metadata")

    return cmd_list


if __name__ == "__main__":
    arguments = parse_arguments()
    logger = get_named_logger(
        name=f"parallel_validation",
        log_level=logging.INFO,
        enable_log_to_file=True,
        project_root=str(ROOT_PATH),
        output_dir="logs",
    )

    model_name = Path(arguments.finetuned_model_id).name
    os.makedirs(ROOT_PATH / "subs", exist_ok=True)
    monitor_csv_path = ROOT_PATH / "subs" / f"monitor_{model_name}.csv"

    # Start monitoring thread
    monitor_thread = threading.Thread(
        target=log_resource_usage,
        args=(monitor_csv_path, arguments.monitor_interval, logger),
        daemon=True,
    )
    monitor_thread.start()

    try:
        main(arguments, logger=logger)
    finally:
        logger.info(">>> Main execution finished. Monitoring thread will stop.")
