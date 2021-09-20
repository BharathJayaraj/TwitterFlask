import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(levelname)s | %(asctime)s | module: %(module)s | lineno: %(lineno)d | %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = TimedRotatingFileHandler(log_file, when='midnight')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


exc = setup_logger('second_logger', 'logs/exceptions.log')
