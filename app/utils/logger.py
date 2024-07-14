import os
import logging

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format='{"severity"="%(levelname)s", "timestamp"="%(asctime)s", "path"="%(pathname)s:%(lineno)d", "message"="%(message)s"}',
    datefmt="%m-%d-%Y %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
