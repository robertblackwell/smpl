import pprint
import os
import json
from typing import Any, Dict

import yaml
from types import SimpleNamespace as Namespace

import smpl.defaults as Defaults
import smpl.util as util
import smpl.object as Object

#
# This file contains functions to read the config file
# and turn it itnot a well defined class instance
#

pp = pprint.PrettyPrinter(indent=4)

PackageSpecificParamaters = Any
Configurations = Dict[str, PackageSpecificParamaters]


def file_get_contents(file_name: str) -> str:
    data = ""
    with open(file_name, 'r') as file:
        #     for line in enumerate(file):
        #         if not isCommentLine(line):
        #             data += line
        # return data
        data = file.read()
    return data


def get_config(file_name: str) -> Configurations:
    config = {}
    """ 
    # reads either a json or yaml file to get part of the config
    # @param string file_name Path for config file
    # @return an object
    """
    ext = os.path.splitext(file_name)[1]
    if ext == ".json":
        d = file_get_contents(file_name)
        jdata = json.loads(d, object_hook=lambda d: Namespace(**d))
    elif ext == ".yaml":
        with open(file_name) as f:
            data = yaml.load(f, Loader=yaml.CLoader)
            # // we are required to return an object and yaml gives us a dctionary
            obj = Object.parse_to_object(data)

            return obj
    else:
        raise ValueError("unknown file extension on config file {}".format(ext))
    return jdata


# parameters for a single package extracted from the config file
# at a min should have a "name" and "version" attribute
class PackageParms:
    def __init__(self, dict_data: Dict):
        # these lines are to silence type warnings when self.name and self.version
        # and to hel[ auto complete
        self.name = ""
        self.version = ""
        if "name" not in dict_data:
            raise ValueError("some dependency entry from the coonfig file does not have a name attribute")

        if "version" not in dict_data:
            raise ValueError("dependency entry from config file name: {} does not have a version".format(self.name))
        self.__dict__ = dict_data

# Config object holds an amalganation of all the data from config_file and
# cli args/options + a number of file path values derived from the config/arg
# data
class ConfigObject:

    # get the parameters for a specific package that are in the dependecies field
    # of the ConfigObject
    def package_parms(self, package_name: str) -> PackageParms:
        if package_name not in self.dependencies:
            raise ValueError("package name {} not found in config file".format(package_name))
        p = self.dependencies[package_name]
        return p

    # constructor
    def __init__(self, cli_args):
        if cli_args.config_file_path is None:
            config = get_config("./smpl.json")
        else:
            config = get_config(cli_args.config_file_path)

        m = Object.merge_objects(config, cli_args)

        if m.project_name is None:
            print("Error: project name is required")
            exit()
        else:
            self.project_name = m.project_name

        if m.project_dir is None:
            self.project_dir = os.getcwd()
        else:
            self.project_dir = m.project_dir

        self.external_name = "external_src"
        self.vendor_name = "vendor"
        self.scripts_name = "scripts"
        self.clone_name = "clone"
        self.stage_name = "stage"
        self.clone_dir = os.path.join(self.project_dir, self.scripts_name, self.clone_name)
        self.stage_dir = os.path.join(self.project_dir, self.scripts_name, self.stage_name)
        self.unpack_dir = os.path.join(self.project_dir, self.scripts_name, self.clone_name)
        self.source_dir = os.path.join(self.project_dir, self.project_name)
        self.external_dir = os.path.join(self.project_dir, self.project_name, self.vendor_name, "src")
        self.vendor_dir = os.path.join(self.project_dir, self.vendor_name)
        self.dependencies = {}

        a = self.project_name.lower()
        b = os.path.basename(self.project_dir).lower()
        xx = (a != b)
        if self.project_name.lower() != os.path.basename(self.project_dir).lower():
            print("project name [%s] and current working directory [%s] have conflict" % (
                self.project_name.lower(), os.path.basename(self.project_dir).lower()))
            exit()

        if m.source_dir_name is None:
            self.source_dir = os.path.join(self.project_dir, self.project_name.lower())
        else:
            self.source_dir = os.path.join(self.project_dir, m.source_dir_name)

        if not os.path.isdir(self.source_dir):
            print("The given source dir [%s] does not exist" % self.source_dir)
            exit()
        if os.path.realpath(os.path.join(self.source_dir, "../")) != self.project_dir:
            print("The given source dir [%s] is not an immediate subdir of the project dir [%s]" % (
                self.source_dir, self.project_dir))
            exit()

        self.script_dir = os.path.join(self.project_dir, 'scripts')
        if hasattr(m, 'clone_dir_path') and m.clone_dir_path:
            self.clone_dir = os.path.abspath(m.clone_dir_path)
        else:
            self.clone_dir = os.path.join(self.script_dir, 'clone')

        if hasattr(m, 'stage_dir_path') and m.stage_dir_path:
            self.stage_dir = os.path.abspath(m.stage_dir_path)
        else:
            self.stage_dir = os.path.join(self.script_dir, 'stage')

        if hasattr(m, 'vendor_dir_path') and m.vendor_dir_path:
            self.vendor_dir = os.path.abspath(m.vendor_dir_path)
        else:
            self.vendor_dir = os.path.join(self.project_dir, 'vendor')

        if hasattr(m, 'external_dir_path') and m.external_dir_path:
            self.external_dir = os.path.abspath(m.external_dir_path)
        else:
            self.external_dir = os.path.join(self.vendor_dir, 'src')

        for d in m.dependencies:
            x = d.__dict__
            if not hasattr(d, "name"):
                raise ValueError("some dependency entry from the coonfig file does not have a name attribute")
            if not hasattr(d, "version"):
                raise ValueError("dependency entry from config file name: {} does not have a version".format(d.name))
            self.dependencies[d.name] = PackageParms(d.__dict__)
