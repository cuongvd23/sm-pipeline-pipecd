import logging

from colorlog import ColoredFormatter


def get_logger(name: str) -> logging.Logger:
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-4s%(reset)s [%(process)d] [%(asctime)s] [%(name)s] %(message)s",
        # datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    _logger = logging.getLogger(name)
    if _logger.hasHandlers():
        _logger.handlers.clear()
    _logger.addHandler(handler)
    _logger.propagate = False
    return _logger
