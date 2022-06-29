import datetime
import logging
from logging import handlers
from os import mkdir
from os.path import isdir, isfile
from pathlib import Path

dir_path = str(Path(__file__).parents[2])


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        # noinspection PyTypeChecker
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Create logger for debugging with a high log level
logger = logging.getLogger("SSMS Package")
logger.setLevel(logging.DEBUG)

# Create console handler with a high log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

# Check if a logs folder exists
isDir = isdir(dir_path + '/logs')
if not isDir == 1:
    mkdir(str(dir_path + '/logs'))

# Create a new log file for each new day and run
filename = dir_path + '/logs/{:%Y-%m-%d}.log'.format(datetime.datetime.now())
perform_roll_over = isfile(filename)
ch = logging.handlers.RotatingFileHandler(filename, backupCount=25)
if perform_roll_over:
    ch.doRollover()

logging.basicConfig(handlers=[logging.handlers.TimedRotatingFileHandler(filename)],
                    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
