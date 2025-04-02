EMPTY_VALUE = "None"

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s, %(name)s, %(levelname)s, %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "logs.json_formatter.JSONLogFormatter",
        },
    },
    "handlers": {
        "console": {
            "formatter": "json",
            "class": "asynclog.AsyncLogDispatcher",
            "func": "logs.json_formatter.write_log",
            "level": "INFO",
        },
        "file": {
            "formatter": "json",
            "class": "asynclog.AsyncLogDispatcher",
            "func": "logs.json_formatter.write_file",
            "level": "ERROR",
        },
    },
    "loggers": {
        "logs": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "WARN",
            "propagate": False,
        },
    },
}
