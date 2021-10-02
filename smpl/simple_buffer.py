import os
from smpl.package import SourcePackage
from smpl.config_file import ConfigObject, PackageParms
import smpl.log_module as logger

class SimpleBuffer(SourcePackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = ""
        self.git_url = "git@github.com:robertblackwell/simple_buffer.git"
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "simple_buffer")
        self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "src")
        self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "simple_buffer")

    def get_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
        self.get_git_repo(self.git_url, "simple_buffer")

    def stage_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
        self.stage_source("simple_buffer", "simple_buffer")

    def install_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
        self.install_stage_to_project("simple_buffer", "simple_buffer")

