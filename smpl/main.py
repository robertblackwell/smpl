import pprint
import os
import sys

import smpl.dispatcher as dispatcher
import smpl.cli_interface as cli_interface
import smpl.util as util
import smpl.exec as exec
import smpl.log_module as logger
import smpl.config_file as configuration
import smpl.log_module as logger


pp = pprint.PrettyPrinter(indent=4)

debug = True
logfile = False

__version__ = "1.0.0"

def main():
    parser = cli_interface.define_cli_interface()

    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)

    cfg_obj: configuration.ConfigObject = configuration.ConfigObject(args)

    #
    # setup logging TODO - wrap in a function in the logger
    #
    logger.init(logger.LOG_LEVEL_DEBUG)
    if args.log_actions:
        if args.log_path is None:
            action_log_path = os.path.abspath("./action_log.log")
            logger.set_logfile(action_log_path)
        elif args.log_path == "stdout":
            logger.set_stdout_logfile()
        else:
            action_log_path = args.log_path
            logger.set_logfile(action_log_path)

        # util.set_log_file(action_log_path, util.LOG_LEVEL_DEBUG)
    exec.configure(arg_reporting_option=exec.REPORTING_OPT_STDOUT_STDERR)
    #
    # now dispatch the subcommand
    #
    dispatcher.dispatch(args.subcmd, args.subcmd_arg, cfg_obj)


if __name__ == "__main__":
    main()
