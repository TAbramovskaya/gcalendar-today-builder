import logging
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "sync.log")


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Returns a logger that writes both to terminal and sync.log
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # Prevent adding multiple handlers if called multiple times
        return logger

    logger.setLevel(logging.INFO)

    # File handler (append mode)
    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    # Stream handler (console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
