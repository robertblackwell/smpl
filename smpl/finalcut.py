import os
import smpl.util as util
import smpl.exec as exec
import smpl.log_module as logger
from smpl.package import LibraryPackage
from smpl.config_file import ConfigObject, PackageParms

class Finalcut(LibraryPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = "v0.6.0"
        self.git_url = "https://github.com/gansm/finalcut.git"
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "finalcut")
        self.git_branch_arg = "stable"
        self.package_stage_include_dir_path = os.path.join(self.cfg_obj.stage_dir, "include", "final")
        self.package_vendor_include_dir_path = os.path.join(self.cfg_obj.vendor_dir, "include", "final")

    def get_package(self):
        self.get_git_repo(self.git_url, "finalcut", self.git_branch_arg)

    def stage_package(self):
        util.clear_directory(self.package_stage_include_dir_path)
        util.rm_file("{}/libfinal*".format(self.stage_lib_dir_path))
        sys_desc = platform.platform()
        if re.search('Linux', sys_desc) is not None \
                and re.search('x86_64', sys_desc) is not None:
            arch_arg = "linux-x86_64"
        elif re.search('Darwin', sys_desc) is not None:
            arch_arg = "darwin64-x86_64-cc"
        else:
            raise RuntimeError("could not determine platform type for finalcut build options - platform is: {}".format(sys_desc))
        exec.run(["autoreconf", "--install", "--force"])
        exec.run(["./configure",
                  "--prefix={}".format(self.cfg_obj.stage_dir),
                  "--debug"
                  # arch_arg,
                  # "linux-x86_64"
                  # "darwin64-x86_64-cc"
                  ],
                 self.package_clone_dir_versioned_path)

        exec.run(["make", "all"], self.package_clone_dir_versioned_path)
        exec.run(["make", "install"], self.package_clone_dir_versioned_path)

    def install_package(self):
        self.headers_from_stage_to_vendor("cert", "cert")
        self.libs_from_stage_to_vendor("libcert.*")

