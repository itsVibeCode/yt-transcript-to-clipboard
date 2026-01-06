# core/logger_setup.py
"""
Centralized logging configuration.
"""

import logging
from typing import Optional


class UILogHandler(logging.Handler):
    """
    Logging handler that forwards logs to MainWindow.
    """

    def __init__(self, ui_window):
        super().__init__()
        self.ui_window = ui_window

    def emit(self, record):
        try:
            message = self.format(record)
            self.ui_window.log(message)
        except Exception:
            self.handleError(record)


def setup_logger(
    ui_window=None,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Setup application-wide logger.

    Args:
        ui_window: MainWindow instance (optional)
        level: logging level

    Returns:
        configured logger
    """
    logger = logging.getLogger("yt_sub_app")
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger  # prevent duplicate handlers

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # UI handler (optional)
    if ui_window is not None:
        ui_handler = UILogHandler(ui_window)
        ui_handler.setFormatter(formatter)
        logger.addHandler(ui_handler)

    return logger


def get_logger() -> logging.Logger:
    """
    Get existing application logger.
    """
    return logging.getLogger("yt_sub_app")
