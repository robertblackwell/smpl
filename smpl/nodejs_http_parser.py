import os
from smpl.package import SourcePackage
from smpl.config_file import ConfigObject, PackageParms

class NodeJsHttpParser(SourcePackage):
    def __init__(self, name: str, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = "v2.9.4"
        self.git_url = "https://github.com/nodejs/http-parser"

        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "http-parser")

    def get_package(self):
        self.get_git_repo(self.git_url, "http-parser", self.release)

    def stage_package(self):
        self.stage_source("http-parser", "http-parser")

    def install_package(self):
        self.install_stage_to_project("http-parser", "http-parser")

