

import logging


def generate_logger(logFileName: str) -> logging.Logger:
    logger = logging.getLogger('spam_application')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logFileName + ".log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    
    return logger

