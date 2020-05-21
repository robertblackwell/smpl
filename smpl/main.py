import pprint
import os
import json
import sys
from typing import Any

import yaml
from types import SimpleNamespace as Namespace

import smpl.dispatcher as dispatcher
import smpl.cli_interface as cli_interface
import smpl.defaults as Defaults
import smpl.util as util
import smpl.object as Object
import smpl.config_file as configuration


pp = pprint.PrettyPrinter(indent=4)

project_name = "marvin++"

__version__ = "0.3.5"

debug = True
logfile = False

#
# def file_get_contents(file_name: str) -> str:
#     data = ""
#     with open(file_name, 'r') as file:
#         #     for line in enumerate(file):
#         #         if not isCommentLine(line):
#         #             data += line
#         # return data
#         data = file.read()
#     return data
#
#
# def get_config(file_name: str) -> Any:
#     """
#     # reads either a json or yaml file to get part of the config
#     # @param string file_name Path for config file
#     # @return an object
#     """
#     ext = os.path.splitext(file_name)[1]
#     if ext == ".json":
#         d = file_get_contents(file_name)
#         jdata = json.loads(d, object_hook=lambda d: Namespace(**d))
#     elif ext == ".yaml":
#         with open(file_name) as f:
#             data = yaml.load(f, Loader=yaml.CLoader)
#             # // we are required to return an object and yaml gives us a dctionary
#             obj = Object.parse_to_object(data)
#
#             return obj
#     else:
#         raise ValueError("unknown file extension on config file {}".format(ext))
#     return jdata
#

def main():
    version = "0.1.0"
    parser = cli_interface.define_cli_interface()

    args = parser.parse_args()
    if args.version is not None:
        print(version)
        sys.exit(0)

    cfg_obj: configuration.ConfigObject = configuration.ConfigObject(args)

    #
    # setup logging TODO - wrap in a function in the logger
    #
    if args.log_actions:
        if args.log_path is None:
            action_log_path = os.path.abspath("./action_log.log")
        else:
            action_log_path = args.log_path

        util.set_log_file(action_log_path)

    #
    # now dispatch the subcommand
    #
    dispatcher.dispatch(args.subcmd, args.subcmd_arg, cfg_obj)


if __name__ == "__main__":
    main()
