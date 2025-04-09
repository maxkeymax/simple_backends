import logging
from logging import Formatter, Logger, StreamHandler


def setup_logger() -> Logger:
    logger: Logger = logging.getLogger("fastapi_app")
    logger.setLevel(logging.DEBUG)

    console_handler: StreamHandler = StreamHandler()
    console_handler.setLevel(logging.ERROR)

    formatter: Formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
