import logging


def init_logger():
    """
    initialize logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', '%H:%M:%S')

    # set console handler settings
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    # set file handler settings
    fh = logging.FileHandler('error.log')
    fh.setLevel(logging.ERROR)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)