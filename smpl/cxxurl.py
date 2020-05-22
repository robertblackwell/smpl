import os
from .package import SourcePackage
from smpl.config_file import ConfigObject, PackageParms

class CxxUrl(SourcePackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = ""
        self.git_url = "git@github.com:robertblackwell/cxxurl.git"
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "cxxurl")
        self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "cxxurl")
        self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "cxxurl")

    def get_package(self):
        self.get_git_repo(self.git_url, "cxxurl")

    def stage_package(self):
        self.stage_source("cxxurl", "cxxurl")

    def install_package(self):
        self.install_stage_to_project("cxxurl", "cxxurl")
