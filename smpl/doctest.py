import os
from smpl.config_file import ConfigObject, PackageParms

from .package import HeadersOnlyPackage


class Doctest(HeadersOnlyPackage):
    def __init__(self, name: str, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        # the name of the directory that the cloned repo will unpack into
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "doctest")
        self.parms = parms

        # the release must match a repo tag
        self.release = "2.3.7"
        self.git_url = "https://github.com/onqtam/doctest.git"
        self.git_branch_arg = "{}".format(self.release)
        # the dir in the repo from where we copy headers
        self.cp_from_here_dir = os.path.join(self.package_clone_dir_path, "doctest")

    def get_package(self):
        self.get_git_repo(self.git_url, "doctest", self.git_branch_arg)

    def stage_package(self):
        self.stage_headers_only_from_repo(repo_name="doctest", stage_name="doctest", repo_sub_directory="doctest")

    def install_package(self):
        self.headers_from_stage_to_vendor("doctest", "doctest")
