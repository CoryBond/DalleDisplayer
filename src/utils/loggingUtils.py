

import logging

from utils.pathingUtils import get_log_directory


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def configureBasicLogger(filename='aiImageDisplayer.log', level=logging.INFO):
    logging.basicConfig(filename=get_log_directory()/filename, encoding='utf-8', format=FORMAT, level=level)    
