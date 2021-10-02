import os
import sys
import subprocess
from typing import Union, TextIO, List, AnyStr
import smpl.log_module as logger

# 
# This module executes commands, manages output from those commands and provides a dry-run capability.
# 
# The primary function is 
# 
#   def run(cmd, where)
# 
# dry-run and output options are controlled by:
# 
#   def configure(arg_dry_run, arg_reporting_option)
# 
# both arguments can ge provided as kw-args and have defaults; no dry-run and report everything
# configure() should be called before any calls to run()
# 
# Output options are:
#   REPORTING_OPTION_STDOUT_STDERR          : simple pass through stdout and stderr  
#   REPORTING_OPTION_STDOUT_ONLY            : simple pass through stdout and show any stderr output only on a failure  
#   REPORTING_OPTION_STDERR_ONLY            : show stderr only on a failure and does not show any stdout  
#   REPORTING_OPTION_NEITHER                : shows no output either from stdout or stderr  
#   REPORTING_OPTION_STDERR_STDOUT_PROGRESS : shows stderr only on a failure and prints an X for each line
#                                             of stdout - does this in realtime while the command is executing  
# 


REPORTING_OPT_STDOUT_STDERR = 1
REPORTING_OPT_STDOUT_ONLY = 2
REPORTING_OPT_STDERR_ONLY = 3
REPORTING_OPT_STDERR_STDOUT_PROGRESS = 5
REPORTING_OPT_NEITHER = 4

class Options:
    def __init__(self):
        self.reporting_option = REPORTING_OPT_STDOUT_ONLY
        self.dry_run = False

options: Options = Options()

def configure(arg_reporting_option = REPORTING_OPT_STDOUT_STDERR, arg_dry_run: bool = False) -> None:
    options.reporting_option = arg_reporting_option
    options.dry_run = arg_dry_run
    logger.debugln("dry_run: {} reporting: {}".format(options.dry_run, options.reporting_option))

def exec_cmd(cmd, where: Union[str, None]) -> None:
    """ Does the hard work of executing commands, optionally in the given directory
    with the reporting global reporting option.

    On failure of the command it quits the program
    """
    logger.debugln(" cmd: {} where: {} dry_run: {}".format(",".join(cmd), where, options.dry_run))
    if options.dry_run:
        return
    if where is None:
        where = os.getcwd()
    try:
        stderr_output = "unassigned"
        if options.reporting_option == REPORTING_OPT_STDOUT_STDERR:
            result = subprocess.run(cmd, cwd = where)
            retcode = result.returncode
        elif options.reporting_option == REPORTING_OPT_STDOUT_ONLY:
            result = subprocess.run(cmd, cwd = where, stderr=subprocess.PIPE)
            retcode = result.returncode
            stderr_output = result.stderr
        elif options.reporting_option == REPORTING_OPT_STDERR_ONLY:
            result = subprocess.run(cmd, cwd = where, stdout=subprocess.PIPE)
            retcode = result.returncode
            stderr_output = result.stderr
        elif options.reporting_option == REPORTING_OPT_STDERR_STDOUT_PROGRESS:
            count = 0
            result = subprocess.Popen(cmd, cwd = where, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while result.poll() is None:
                if count == 0:
                    sys.stdout.write("\n")
                stdoutline = result.stdout.readline()
                sys.stdout.write("X")
                count = (count + 1) % 50
            flush = result.stdout.read()
            sys.stdout.write("YY\n")
            # sys.stdout.write("\n")
            
            result.stdout.close()
            # print("result.stdout closed")
            retcode = result.returncode
            stderr_output = result.stderr
        else:
            result = subprocess.run(cmd, cwd = where, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            retcode = result.returncode
            stderr_output = result.stderr
        if retcode > 0:
            sys.stderr.write("ERROR cmd: {} return code {}\n".format(", ".join(cmd), retcode))
            sys.stderr.write("stderr {}\n".format(stderr_output))
            raise RuntimeError("bad return code")

    except Exception as exception:
        sys.stderr.write("Cmd was {}\n".format(", ".join(cmd)))
        sys.stderr.write(
            "An error occurred while running command [{}] error type: {}\n".format(", ".join(cmd), type(exception).__name__)) 
        sys.stderr.write("Details: \n{}\n".format(str(exception)))
        quit()


def run(cmd: List[str], where: Union[str, None] = None) -> None:
    logger.debugln(" cmd: {} where: {}".format(",".join(cmd), where))
    if not isinstance(cmd, list):
        raise ValueError("cmd must be a list")
    # exec_cmd handles failure of the command
    exec_cmd(cmd, where)

if __name__ == '__main__':
    logger.init(logger.LOG_LEVEL_WARN)
    logger.set_stdout_logfile()
    configure(arg_dry_run=False, arg_reporting_option=REPORTING_OPT_STDOUT_ONLY)
    run(["wget", "http://whiteacorn.com"], None)
    run(["tree", "/home/robert/Projects/smpl"])
    configure(arg_dry_run=False, arg_reporting_option=REPORTING_OPT_STDERR_STDOUT_PROGRESS)
    run(["tree", "/home/robert/Projects/smpl"])
    configure(arg_dry_run=False, arg_reporting_option=REPORTING_OPT_STDOUT_ONLY)
    run(["tree", "/xhome/robert/Projects/smpl"])
