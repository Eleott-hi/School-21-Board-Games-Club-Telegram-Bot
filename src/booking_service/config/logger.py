from datetime import date
import logging
import logging.config
from config.config import LOG_LEVEL

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "format": "%(log_color)s%(levelname)s: %(asctime)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "colorlog.ColoredFormatter",
        },
        "simple": {
            "format": "%(levelname)s: %(asctime)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "logs/log",
            "when": "S",
            "interval": 1,
            "backupCount": 10,
        },
    },
    "loggers": {
        "": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file"],
        }
    },
}



logging.config.dictConfig(LOGGER_CONFIG)
