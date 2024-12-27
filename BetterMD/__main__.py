import logging


def setup_logger():
    LEVEL = logging.INFO
    logging.basicConfig(level=LEVEL)
    logger = logging.getLogger("BetterMD")
    return logger

setup_logger()