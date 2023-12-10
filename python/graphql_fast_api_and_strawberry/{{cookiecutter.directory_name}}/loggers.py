from typing import Optional, List
import logging.config

_STATE = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {},
}


def get_logger(name: str, level: str = "INFO", handlers: Optional[List[str]] = None):
    if handlers is None or len(handlers) == 0:
        handlers = ["default"]
    _STATE["loggers"][name] = {"handlers": handlers, "level": level}
    logging.config.dictConfig(_STATE)
    return logging.getLogger(name)
