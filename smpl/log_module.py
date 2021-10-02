import os
import sys
import subprocess
import shutil
import re
import pprint
from typing import Union, TextIO, List, AnyStr

LOG_LEVEL_WARN = 1
LOG_LEVEL_INFO = 2
LOG_LEVEL_DEBUG = 3

def caller_name() -> str:
    fn = os.path.basename(sys._getframe(2).f_code.co_filename).split(".")[0]
    cn = sys._getframe(2).f_code.co_name
    return [fn, cn]

class Logger:
    def __init__(self):
        self.enabled: bool = False
        self.log_file_path: str = 'action_log.log'
        self.log_file = None

    def open(self, level) -> None:
        self.enabled = True
        if level < LOG_LEVEL_WARN or level > LOG_LEVEL_DEBUG:
            raise ValueError("invalid log level {}".format(level))
        self.level = level
        self.log_file: TextIO = open(self.log_file_path, "w+")

    def write(self, text: str) -> None:
        if self.enabled:
            self.log_file.write(text)

    def writeln(self, line: str) -> None:
        if self.enabled:
            self.log_file.write(line + "\n")

logger: Union[Logger, None] = Logger()
log_file_path = ""
log_file = None
def set_log_file(logfile_path, level):
    logger.log_file_path = logfile_path
    logger.open(level)

def set_stdout_logfile():
    logger.log_file = sys.stdout

def set_default_logfile():
    logger.log_file_path = 'action_log.log'
    logger.log_file = open(logger.log_file_path, "w+")

def set_logfile(log_file_name):
    logger.log_file_path = log_file_name
    logger.log_file = open(logger.log_file_path, "w+")


def init(level):
    """This function must becalled before using the logger. Typically in the main initialization """
    logger.open(level)

def writeln(text: str) -> None:
    logger.writeln(text)    

def write(text: str) -> None:
    logger.write(text)    

def info(text: str) -> None:
    cn = caller_name();
    if(logger.level >= LOG_LEVEL_INFO):
        logger.write("{}.{} {}".format(cn[0], cn[1], text))

def infoln(text: str) -> None:
    cn = caller_name();
    if(logger.level >= LOG_LEVEL_INFO):
        logger.writeln("{}.{} {}".format(cn[0], cn[1], text))

def warn(text: str) -> None:
    cn = caller_name();
    if(logger.level >= LOG_LEVEL_WARN):
        logger.write("{}.{} {}".format(cn[0], cn[1], text))

def warnln(text: str) -> None:
    cn = caller_name();
    if(logger.level >= LOG_LEVEL_WARN):
        logger.writeln("{}.{} {}".format(cn[0], cn[1], text))

def debug(text: str) -> None:
    cn = caller_name();
    if(logger.level >= LOG_LEVEL_DEBUG):
        logger.write("{}.{} {}".format(cn[0], cn[1], text))

def debugln(text: str) -> None:
    cn = caller_name();
    if(logger.level >= LOG_LEVEL_DEBUG):
        logger.writeln("{}.{} {}".format(cn[0], cn[1], text))

