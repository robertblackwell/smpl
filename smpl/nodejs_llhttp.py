import os
from smpl.package import SourcePackage
from smpl.config_file import ConfigObject, PackageParms
import smpl.util as util
#
# llhttp is a project in which some of thec source code is generated.
# to make it run
#   make release
# the all the code is in release/include and release/src
#
# to make it work in a hostng project all of the code both .h and .c
#  must end up in vendor/src/llhttp/*.c *.h
#
class NodeJsLLHttp(SourcePackage):
    def __init__(self, name: str, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = "v2.2.0"
        self.git_url = "https://github.com/nodejs/llhttp"

        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "llhttp")

    def build_in_clone(self):
        # this package require the source and headers to be generated
        util.run(["npm", "install"], self.package_clone_dir_path)
        util.run(["make", "release"], self.package_clone_dir_path)
        # util.run(["make", "install"], self.package_clone_dir_versioned_path)

        pass

    def get_package(self):
        self.get_git_repo(self.git_url, "llhttp", self.release)
        self.build_in_clone()

    def stage_package(self):
        self.stage_source("llhttp/release/include", "llhttp/src")
        self.stage_source("llhttp/release/src", "llhttp/src")

    def install_package(self):
        # had to trick it into doing the right thing
        self.install_stage_to_project("llhttp/include", "../src/llhttp")
        self.install_stage_to_project("llhttp/src", "../src/llhttp", False)

