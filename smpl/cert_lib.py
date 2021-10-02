import os
import smpl.util as util
import smpl.exec as exec
import smpl.log_module as logger
from smpl.package import LibraryPackage
from smpl.config_file import ConfigObject, PackageParms

class CertLib(LibraryPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, name));
        super().__init__(name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = "v0.1.0"
        self.git_url = "https://github.com/robertblackwell/x509_certificate_library.git"
        self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, "x509_certificate_library")
        self.git_branch_arg = self.release
        self.package_stage_include_dir_path = os.path.join(self.cfg_obj.stage_dir, "include", "cert")
        self.package_vendor_include_dir_path = os.path.join(self.cfg_obj.vendor_dir, "include", "cert")
        self.cmake_dir = os.path.join(self.package_clone_dir_path, "cmake-build-debug")

    def get_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name));
        self.get_git_repo(self.git_url, "x509_certificate_library", self.git_branch_arg)

    def stage_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name));
        util.mkdir_p(self.stage_include_dir_path)
        util.mkdir_p(self.stage_lib_dir_path)

        util.clear_directory(self.package_stage_include_dir_path)
        util.rm_directory_contents(self.stage_lib_dir_path, "libcert.*")
        # exec.run(["rm", "-rf",  "{}/libcert*".format(self.stage_lib_dir_path)])

        self.cmake_dir = os.path.join(self.package_clone_dir_path, "cmake-build-debug")
        util.clear_directory(self.cmake_dir)
        exec.run([
            "cmake",
            "-DVENDOR_DIR={}".format(self.cfg_obj.stage_dir),
            "-DSTAGE_DIR={}".format(self.cfg_obj.stage_dir),
            ".."
        ], self.cmake_dir)
        exec.run([
            "make",
            "-j30",
            "cert_library"
        ], self.cmake_dir)
        exec.run([
            "cmake",
            "--build",
            ".",
            "--target",
            "install",
            "-j", "8"
        ], self.cmake_dir)
        # just installed the headers into stage/include/cert
        logger.writeln("CertLib stage_package end")

    def install_package(self):
        logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name));
        self.headers_from_stage_to_vendor("cert", "cert")
        self.libs_from_stage_to_vendor("libcert.*")

