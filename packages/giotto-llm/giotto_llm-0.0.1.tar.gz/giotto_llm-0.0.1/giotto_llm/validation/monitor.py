import csv
import logging
import time
from datetime import datetime

import GPUtil
import psutil

from giotto_llm.consts import ROOT_PATH
from giotto_llm.logs import get_named_logger


def log_resource_usage(log_file_path: str, interval_s: float, logger: logging.Logger) -> None:
    # Detect GPUs and prepare headers
    gpus = GPUtil.getGPUs()
    gpu_usage_headers = [f"GPU_{i}_Usage(%)" for i in range(len(gpus))]
    gpu_memory_headers_mb = [f"GPU_{i}_Memory_Used(MB)" for i in range(len(gpus))]
    gpu_memory_headers_percent = [f"GPU_{i}_Memory_Used(%)" for i in range(len(gpus))]

    headers = (
        ["Timestamp", "CPU_Usage(%)", "RAM_Usage(%)", "RAM_Used(MB)"]
        + gpu_usage_headers
        + gpu_memory_headers_mb
        + gpu_memory_headers_percent
    )

    with open(log_file_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

    logger.info(f">>> Logging resource usage to {log_file_path} every {interval_s} seconds...")

    while True:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get RAM usage
        ram_info = psutil.virtual_memory()
        ram_usage_percent = ram_info.percent
        ram_used_mb = ram_info.used / (1024**2)  # Convert to MB

        # Get GPU usage for each available GPU
        gpus = GPUtil.getGPUs()
        gpu_usage_data = []
        for gpu in gpus:
            gpu_usage_data.append(gpu.load * 100)  # GPU usage percentage
        for gpu in gpus:
            gpu_usage_data.append(gpu.memoryUsed)  # GPU memory usage in MB
        for gpu in gpus:
            gpu_usage_data.append(
                gpu.memoryUsed * 100.0 / gpu.memoryTotal
            )  # GPU memory usage in MB

        row = [timestamp, cpu_usage, ram_usage_percent, ram_used_mb] + gpu_usage_data

        # Append the stats to the CSV file
        with open(log_file_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        # Wait for the specified interval
        time.sleep(interval_s)


if __name__ == "__main__":
    log_file_path = "resource_usage_log.csv"
    interval = 2

    logger = get_named_logger(
        name=f"monitor",
        log_level=logging.INFO,
        enable_log_to_file=True,
        project_root=str(ROOT_PATH),
        output_dir="logs",
    )

    log_resource_usage(log_file_path, interval_s=interval, logger=logger)
