import sys, os
import logging, colorlog

LOG_COLORS = {'DEBUG':'cyan', 'INFO':'green', 'TRAIN':'blue', 'WARNING':'yellow', 'ERROR': 'red', 'CRITICAL':'red,bg_white'}
LOG_LEVELS = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "TRAIN": 25, "INFO": 20, "DEBUG": 10, "NOTSET": 0}

if logging.getLevelName(LOG_LEVELS["TRAIN"]) != "TRAIN":
    logging.addLevelName(LOG_LEVELS["TRAIN"], 'TRAIN')

def get_logger(name="trainer", level=None, splitsec=False):
    if level is None:
        level = os.environ.get("LOGLEVEL", "INFO")
    handler = colorlog.StreamHandler(stream=sys.stdout)
    log_format = '%(log_color)s%(asctime)s [%(levelname)s] %(white)s(%(name)s)%(reset)s: %(message)s'
    if splitsec:
        log_format = '%(log_color)s%(asctime)s.%(msecs)03d [%(levelname)s] %(white)s(%(name)s)%(reset)s: %(message)s'
    handler.setFormatter(colorlog.ColoredFormatter(log_format,
                                                   log_colors=LOG_COLORS,
                                                   datefmt="%H:%M:%S",
                                                   stream=sys.stdout))

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.train = lambda message: logger.log(LOG_LEVELS["TRAIN"], message)
    logger.setLevel(LOG_LEVELS[level])

    return logger
