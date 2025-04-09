import logging
from logging import StreamHandler, Formatter

def setup_logger():
    logger = logging.getLogger('fastapi_app')
    logger.setLevel(logging.DEBUG)

    console_handler = StreamHandler()
    console_handler.setLevel(logging.ERROR)

    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
