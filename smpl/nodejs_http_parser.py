import os
from .package import SourcePackage

class NodeJsHttpParser(SourcePackage):
    def __init__(self, name: str, parms, the_defaults):
        super().__init__(name, the_defaults)
        self.name = name
        self.parms = parms
        self.release = "v2.9.4"
        self.git_url = "https://github.com/nodejs/http-parser"

        self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "http-parser")

    def get_package(self):
        self.get_git_repo(self.git_url, "http-parser", self.release)

    def stage_package(self):
        self.stage_source("http-parser", "http-parser")

    def install_package(self):
        self.install_stage_to_project("http-parser", "http-parser")

