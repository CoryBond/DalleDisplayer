

import logging
from logging.handlers import RotatingFileHandler

from utils.pathingUtils import get_or_create_log_directory


FORMAT = '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'


def configureBasicLogger(filename='aiImageDisplayer.log', level=logging.INFO):
    """
    Configures python logging.
    """
    handlers = [RotatingFileHandler(filename=get_or_create_log_directory()/filename, maxBytes=100000, backupCount=3)]
    logging.basicConfig(encoding='utf-8', format=FORMAT, level=level, handlers=handlers)    
