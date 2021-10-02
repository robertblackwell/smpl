import os
import smpl.util as util
import smpl.log_module as logger
from smpl.package import HeadersOnlyPackage
from smpl.config_file import ConfigObject, PackageParms

supported_version = {
    "v2.0.0": "",
    "v3.0.0": "",
    "V3.0.0": ""
}


class Trog(HeadersOnlyPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, name));
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        if parms.version not in supported_version:
            raise ValueError("version {} not supported".format(parms.version))
        self.release = parms.version
        self.git_url = "https://github.com/robertblackwell/trog.git"
        self.git_branch_arg = self.release
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "trog")
        self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "trog")
        # self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "trog")

    def get_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
        self.get_git_repo(self.git_url, "trog", self.git_branch_arg)

    def stage_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
        self.stage_headers_only_from_repo(repo_name="trog", stage_name="trog",
                                          repo_sub_directory="include/trog")

    def install_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
        self.headers_from_stage_to_vendor("trog", "trog")
