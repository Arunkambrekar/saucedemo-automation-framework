import logging
import os

def get_logger(name="framework"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        log_path = os.path.join("logs", "automation.log")
        file_handler = logging.FileHandler(log_path, mode="a")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
