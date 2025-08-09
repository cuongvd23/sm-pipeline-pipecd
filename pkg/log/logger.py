import logging

from colorlog import ColoredFormatter


def get_logger(name: str) -> logging.Logger:
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-4s%(reset)s [%(process)d] %(name)s %(message)s",
        datefmt=None,
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
    _logger.addHandler(handler)
    return _logger
