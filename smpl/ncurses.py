import os
import smpl.util as util
import smpl.log_module as logger
from smpl.package import LibraryPackage
from smpl.config_file import ConfigObject, PackageParms
import smpl.exec as exec

supported_versions = {
    "6.2": {
        "url": "https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.2.tar.gz",
        "targz": "ncurses-6.2.tar.gz",
        "repo_name": "ncurses-6.2"
    }
}


class NCurses(LibraryPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        if parms.version not in supported_versions:
            v = ", ".join(supported_versions.keys())
            raise ValueError(
                "config file specifies ncurses version {} can only install version {}".format(parms.version, v))
        vers = parms.version
        self.name = name
        self.parms = parms
        self.release = vers
        self.package_url = supported_versions[vers]['url']
        self.targz = supported_versions[vers]['targz']
        self.repo_name = supported_versions[vers]['repo_name']

        self.package_targz_file_path = os.path.join(self.cfg_obj.clone_dir, self.targz)
        self.wget_output_path = os.path.join(self.cfg_obj.clone_dir, self.targz)
        self.package_targz_file_path = os.path.join(self.cfg_obj.clone_dir, self.targz)
        self.clone_dir_path = os.path.join(self.cfg_obj.clone_dir, self.repo_name)

    def get_package(self):
        self.get_and_unpack_tar(self.package_url, self.targz, self.repo_name)

    def stage_package(self):
        logger.writeln("NCurses stage_package begin")
        util.mkdir_p(self.stage_include_dir_path)

        # make sure stage/include/boost exists and is empty
        util.mkdir_p(self.package_stage_include_dir_path)
        util.rm_directory_contents(self.package_stage_include_dir_path)

        util.mkdir_p(self.stage_lib_dir_path)

        exec.run(["rm", "-rf", "{}/libncurses*".format(self.stage_lib_dir_path)])
        exec.run(["rm", "-rf", "{}/libform*".format(self.stage_lib_dir_path)])
        exec.run(["rm", "-rf", "{}/libmenu*".format(self.stage_lib_dir_path)])
        exec.run(["rm", "-rf", "{}/libform*".format(self.stage_lib_dir_path)])

        exec.run([
            "./configure",
            "--prefix={}".format(self.cfg_obj.vendor_dir),
            "--enable-sigwinch",
            "--with-normal",
            "--with-pthread",
            "--with-debug"
        ], self.clone_dir_path)
        exec.run(
            ['make'], self.clone_dir_path
        )

        # exec.run([
        #     "make",
        #     "install"
        # ], self.clone_dir_path
        # )

        logger.writeln("NCurses stage_package end")

    def install_package(self):
        exec.run([
            "make",
            "install"
        ], self.clone_dir_path
        )

        # self.headers_from_stage_to_vendor("ncurses", "ncurses")
        # self.libs_from_stage_to_vendor("libncurse*.*")
        # self.libs_from_stage_to_vendor("libpanel*.*")
        # self.libs_from_stage_to_vendor("libform*.*")
        # self.libs_from_stage_to_vendor("libmenu*.*")
