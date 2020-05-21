import os
from .package import SourcePackage


class CxxUrl(SourcePackage):
    def __init__(self, name, parms, the_defaults):
        super().__init__(name, the_defaults)
        self.name = name
        self.parms = parms
        self.release = ""
        self.git_url = "git@github.com:robertblackwell/cxxurl.git"
        self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "cxxurl")
        self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "cxxurl")
        self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "cxxurl")

    def get_package(self):
        self.get_git_repo(self.git_url, "cxxurl")

    def stage_package(self):
        self.stage_source("cxxurl", "cxxurl")

    def install_package(self):
        self.install_stage_to_project("cxxurl", "cxxurl")
