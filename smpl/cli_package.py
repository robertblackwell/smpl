import os
from .package import HeadersOnlyPackage
from smpl.config_file import ConfigObject, PackageParms

class CLIPackage(HeadersOnlyPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        package_name = name

        parms.repo_name = "CLI11"
        parms.repo_branch_argument = "v1.9.0"
        parms.stage_name = "CLI11"
        parms.vendor_name = "CLI11"
        parms.repo_sub_directory = "single_include/catch2"

        super().__init__(package_name, cfg_obj)
        self.name = name
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "CLI11")
        self.parms = parms
        self.release = "v1.9.0"
        self.git_url = "https://github.com/CLIUtils/CLI11.git"
        self.git_branch_arg = self.release
        self.single_include_dir = os.path.join(self.package_clone_dir_path, "single_include")

    def get_package(self):
        self.get_git_repo(self.git_url, "CLI11", self.git_branch_arg)

    def stage_package(self):
        self.stage_headers_only_from_repo(repo_name="CLI11", stage_name="CLI",
                                          repo_sub_directory="include/CLI")

    def install_package(self):
        self.headers_from_stage_to_vendor("CLI", "CLI")

