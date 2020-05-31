import os
from smpl.package import HeadersOnlyPackage
from smpl.config_file import ConfigObject, PackageParms

supported_version = {
    "v2.0.0": "",
    "v3.0.0": ""
}


class Trog(HeadersOnlyPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        if parms.version not in supported_version:
            raise ValueError("version {} not supported".format(parms.version))
        self.release = parms.version
        self.git_url = "git@github.com:robertblackwell/trog.git"
        self.git_branch_arg = self.release
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "trog")
        self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "trog")
        # self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "trog")

    def get_package(self):
        self.get_git_repo(self.git_url, "trog", self.git_branch_arg)

    def stage_package(self):
        self.stage_headers_only_from_repo(repo_name="trog", stage_name="trog",
                                          repo_sub_directory="include/trog")

    def install_package(self):
        self.headers_from_stage_to_vendor("trog", "trog")
