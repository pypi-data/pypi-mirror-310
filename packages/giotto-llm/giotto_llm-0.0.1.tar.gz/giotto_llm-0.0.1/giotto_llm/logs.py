import logging
import os
import sys


def get_named_logger(
    name: str,
    log_level: int,
    enable_log_to_file: bool,
    project_root: str,
    output_dir: str = "logs",
) -> logging.Logger:
    """Create a Python logger that can log information to STDERR and to a file."""
    # Named logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # sys.stderr handler
    ch_stderr = logging.StreamHandler(stream=sys.stderr)
    ch_stderr.setLevel(log_level)
    formatter_stderr = logging.Formatter(
        fmt="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%H:%M:%S",
    )
    ch_stderr.setFormatter(formatter_stderr)
    logger.addHandler(ch_stderr)

    # File handler (optional)
    if enable_log_to_file:
        # Note: create the logging directory if it doesn't exist
        log_dir_path = os.path.join(project_root, output_dir)
        os.makedirs(log_dir_path, exist_ok=True)

        log_file_path = os.path.join(project_root, output_dir, f"logs")
        ch_file = logging.FileHandler(filename=log_file_path, encoding="utf-8")
        ch_file.setLevel(log_level)
        formatter_file = logging.Formatter(
            fmt="%(asctime)s - %(name)s | %(levelname)s:%(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
        )
        ch_file.setFormatter(formatter_file)
        logger.addHandler(ch_file)

    return logger
