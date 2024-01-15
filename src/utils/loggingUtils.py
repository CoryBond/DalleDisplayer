

import logging

from utils.pathingUtils import get_or_create_log_directory


FORMAT = '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'


def configureBasicLogger(filename='aiImageDisplayer.log', level=logging.INFO):
    """
    Configures python logging.

    TODO: Currently does not support rotating or cleaning old logs.
    """
    logging.basicConfig(filename=get_or_create_log_directory()/filename, encoding='utf-8', format=FORMAT, level=level)    
