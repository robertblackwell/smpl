import os
import smpl.util as util
from smpl.package import LibraryPackage
from smpl.config_file import ConfigObject, PackageParms

supported_versions = {
    "1.72.0": {
        "url": "https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.tar.gz",
        "targz": "boost_1_72_0.tag.gz",
        "repo_name": "boost_1_72_0"
    },

    "1.71.0": {
        "url": "https://dl.bintray.com/boostorg/release/1.71.0/source/boost_1_71_0.tar.gz",
        "targz": "boost_1_71_0.tag.gz",
        "repo_name": "boost_1_71_0"
    }
}


# boost_release = "1.72.0"
# package_url = "https://dl.bintray.com/boostorg/release/{}/source/boost_1_72_0.tar.gz".format(boost_release)
# package_targz_file = "boost_1_72_0.tar.gz"


class Boost(LibraryPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(name, cfg_obj)
        if parms.version not in supported_versions:
            v = ", ".join(supported_versions.keys())
            raise ValueError(
                "config file specifies boost version {} can only install version {}".format(parms.version, v))
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
        util.logger.writeln("Boost stage_package begin")
        util.mkdir_p(self.stage_include_dir_path)

        # make sure stage/include/boost exists and is empty
        util.mkdir_p(self.package_stage_include_dir_path)
        util.rm_directory_contents(self.package_stage_include_dir_path)

        util.mkdir_p(self.stage_lib_dir_path)

        util.run(["rm", "-rf", "{}/libboost*".format(self.stage_lib_dir_path)])

        util.run([
            "./bootstrap.sh",
            "--prefix={}".format(self.cfg_obj.stage_dir),
            "darwin64-x86_64-cc"
        ], self.clone_dir_path)
        util.run([
            "./b2",
            "install",
            "--link=static",
            "--threading=multi",
            "--variant=debug",
            "--layout=system",
        ], self.clone_dir_path)
        util.logger.writeln("Boost stage_package end")

    def install_package(self):
        self.headers_from_stage_to_vendor("boost", "boost")
        self.libs_from_stage_to_vendor("libboost.*")
