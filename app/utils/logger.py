import logging

logging.basicConfig(
    level=logging.INFO,
    format='{"severity"="%(levelname)s", "timestamp"="%(asctime)s", "path"="%(pathname)s:%(lineno)d", "message"="%(message)s"}',
    datefmt="%m-%d-%Y %H:%M:%S",
)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger
