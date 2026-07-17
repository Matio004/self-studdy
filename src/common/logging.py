import json
import logging
import logging.config

from logging import getLogger


class JsonFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__("%(message)s", *args, **kwargs)

    def format(self, record: logging.LogRecord):
        message_dict = {
            "level": record.levelname,
            "timestamp": self.formatTime(record),
            "message": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno,
        }
        return json.dumps(message_dict)


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
)
