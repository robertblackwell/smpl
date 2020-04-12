#!/usr/bin/env python3

import sys
import argparse
import datetime
import pprint
import optparse
import os
import subprocess
import json
from types import SimpleNamespace as Namespace

from .boost import Boost
from .openssl import OpenSSL
from .simple_buffer import SimpleBuffer
from .trog import Trog
from .http_parser import HttpParser
from .uri_parser import UriParser
from .cxxurl import CxxUrl
from .catch2 import Catch2
from .util import set_log_file

pp = pprint.PrettyPrinter(indent=4)

project_name = "marvin++"
# project_dir = os.getcwd()
# source_dir = os.path.join(project_dir, "marvin")
# clone_dir = os.path.join(project_dir, "scripts", "clone")
# stage_dir = os.path.join(project_dir, "scripts", "stage")

__version__ = "0.3.5"

debug = True
logfile = False


def file_get_contents(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    return data


def get_config(file_name):
    d = file_get_contents(file_name)
    jdata = json.loads(d, object_hook=lambda d: Namespace(**d))
    return jdata


def merge_objects(obj1, obj2):
    """
    obj1 is from the json config file and may have keys missing.
    obj2 is from argparse and will have a value(maybe None) for all valid keys
    updates obj1 with values in obj2 where obj1 either does not have that key or the value for the key is None.
    Require obj1 to have a value or None for all valid arg/options
    """
    d2 = obj2.__dict__
    keys = list(d2.keys())
    for k in keys:
        v = obj2.__dict__[k]
        if not (k in obj1.__dict__.keys()):
            obj1.__dict__[k] = v
        elif obj1.__dict__[k] is None:
            obj1.__dict__[k] = v

    return obj1



class Defaults:
    def __init__(self, the_project_name, the_project_dir):
        self.project_name = the_project_name
        self.project_dir = the_project_dir
        self.clone_name = "clone"
        self.stage_name = "stage"
        self.external_name = "external"
        self.vendor_name = "vendor"
        self.scripts_name = "scripts"
        self.unpack_dir = os.path.join(the_project_dir, self.scripts_name, self.clone_name)
        self.source_dir = os.path.join(the_project_dir, the_project_name)
        self.external_dir = os.path.join(the_project_dir, the_project_name, self.external_name)
        self.vendor_dir = os.path.join(the_project_dir, self.vendor_name)


def validate_and_construct_names(args):
    if args.project_name is None: 
        print("Error: project name is required")
        exit()
    if args.project_dir is None: 
        project_dir = os.getcwd()
    else:
        project_dir = args.project_dir

    defaults = Defaults(args.project_name, project_dir)

    a = defaults.project_name.lower()
    b = os.path.basename(defaults.project_dir).lower()
    xx = (a != b)
    if defaults.project_name.lower() != os.path.basename(defaults.project_dir).lower():
        print("project name [%s] and current working directory [%s] have conflict" % (defaults.project_name.lower(), os.path.basename(defaults.project_dir).lower()))
        exit()

    if args.source_dir_name is None:
        defaults.source_dir = os.path.join(defaults.project_dir, defaults.project_name.lower())
    else:
        defaults.source_dir = os.path.join(defaults.project_dir, args.source_dir_name)

    if not os.path.isdir(defaults.source_dir):
        print("The given source dir [%s] does not exist" % defaults.source_dir)
        exit()
    if os.path.realpath(os.path.join(defaults.source_dir, "../")) != defaults.project_dir:
        print("The given source dir [%s] is not an immediate subdir of the project dir [%s]" % (defaults.source_dir, defaults.project_dir))
        exit()

    defaults.script_dir = os.path.join(defaults.project_dir, 'scripts')
    defaults.clone_dir = os.path.join(defaults.script_dir, 'clone')
    defaults.stage_dir = os.path.join(defaults.script_dir, 'stage')
    defaults.vendor_dir = os.path.join(defaults.project_dir, 'vendor')
    defaults.external_dir = os.path.join(defaults.source_dir, 'external')
    return defaults


def action(name, version, defaults):
    print("installing: %s %s " % (name, version))
    if name == "boost":
        handler = Boost(name, version, defaults)
    elif name == "openssl":
        handler = OpenSSL(name, version, defaults)
    elif name == "simple_buffer":
        handler = SimpleBuffer(name, version, defaults)
    elif name == "trog":
        handler = Trog(name, version, defaults)
    elif name == "http_parser":
        handler = HttpParser(name, version, defaults)
    elif name == "uri-parser":
        handler = UriParser(name, version, defaults)
    elif name == "cxxurl":
        handler = CxxUrl(name, version, defaults)
    elif name == "catch2":
        handler = Catch2(name, version, defaults)
    else:
        return
    handler.get_package()
    handler.stage_package()
    handler.install_package()


def doit(openssl_version, output_dir, dryrun_flag):
    print("Hello")
    pp.pprint([openssl_version, output_dir, dryrun_flag])


def main():

    parser = argparse.ArgumentParser(
        description="Install dependencies for project.")
    parser.add_argument('-v', '--version',  action="store_true",
                        help="Prints the version number.")

    parser.add_argument('--install',    dest="install_flag", action="store_true",
                        help='Installs the staged install to the final destination')

    parser.add_argument('--project-name',      dest='project_name', help='The name of the project. Required')
    parser.add_argument('--project-dir',       dest='project_dir', help='Path to the project top level directory. Defaults to pwd. ')
    parser.add_argument('--source-dir-name',   dest='source_dir_name', help='Stem name of the project source directory, should be same as project name lowercased')

    parser.add_argument('--clone-dir',      dest='clone_dir_path', help='The path for directory into which packages are cloned/unpacked. Default to scripts/clone_dir ')
    parser.add_argument('--stage-dir',      dest='stage_dir_path', help='The path for directory into which package headers amd archives are copied after building.'
            + 'Default to scripts/stage ')
    parser.add_argument('--vendor-dir',      dest='vendor_dir_path', help='The path for directory into which package headers amd archives are installed locally to the project.\n'
            +'Mustb always be an immediate subdirectory of the project-dir and defaults to {project-dir}/vendor.')
    parser.add_argument('--external-dir',      dest='external_dir_path', help='The path for directory into packages delivered as copied source files will be installed.\n'
        'Must be inside the project source directory, Defaults to project_dir/source_dir_name/external.')

    parser.add_argument('--config-file',      dest='config_file_path', 
        help='Path of a json config file, alternative to command line options.\n Default duh.json')
    parser.add_argument('--log-actions',      dest='log_actions', action='store_true', help='creates a log of all cli commands ')
    parser.add_argument('--action-logfile',   dest='log_path', help='path of file for logging actions. Default ./action_log.log')
    args = parser.parse_args()
    config = "" #if args.config_file_path is None else get_config(args.config_file_path)
    if args.config_file_path is None:
        config = get_config("./duh.json")
    else:
        config = get_config(args.config_file_path)

    if args.log_actions:
        if args.log_path is None:
            action_log_path = os.path.abspath("./action_log.log")
        else:
            action_log_path = args.log_path

        set_log_file(action_log_path)

    m = merge_objects(config, args)
    dependencies = m.dependencies
    defaults = validate_and_construct_names(m)
    
    pp.pprint(defaults)
    pp.pprint(dependencies)
    for d in dependencies:
        action(d.name, d.version, defaults)


if __name__ == "__main__":
    main()
