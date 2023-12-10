import logging.config


def configure_logger(debug: bool) -> None:
    level = "DEBUG" if debug else "INFO"

    logging.config.dictConfig({
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(message)s (%(name)s)"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
            }
        },
        "loggers": {
            "": {"handlers": ["console"], "level": level},
        },
        "version": 1,
    })
