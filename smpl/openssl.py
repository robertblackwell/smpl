import os
import smpl.util as util
import platform
import re
from smpl.package import LibraryPackage
from smpl.config_file import ConfigObject, PackageParms

package_name = "openssl"
openssl_name = "openssl-1.1.1f"

# package_url = "https://dl.bintray.com/boostorg/release/{}/source/boost_1_72_0.tar.gz".format(boost_release)
package_url = "https://www.openssl.org/source/{}.tar.gz".format(openssl_name)
package_targz_file = "{}.tar.gz".format(openssl_name)
# package_targz_file = "tar xvzf {}.tar.gz".format(openssl_name)


class OpenSSL(LibraryPackage):
    def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
        super().__init__(package_name, cfg_obj)
        self.name = name
        self.parms = parms
        self.release = "1.1.1f"
        self.package_url = "https://www.openssl.org/source/{}.tar.gz".format(openssl_name)

        self.package_targz_file_path = os.path.join(self.cfg_obj.clone_dir, package_targz_file)
        self.wget_output_path = self.cfg_obj.clone_dir
        self.package_targz_file_path = os.path.join(self.cfg_obj.clone_dir, package_targz_file)
        self.vendor_ssl_dir = os.path.join(self.cfg_obj.vendor_dir, "ssl")
        self.package_clone_dir_versioned_path = os.path.join(self.cfg_obj.clone_dir, "openssl-1.1.1f")

    def get_package(self):
        self.get_and_unpack_tar(package_url, package_targz_file, openssl_name)

    def stage_package(self):
        util.clear_directory(self.package_stage_include_dir_path)
        util.rm_file("{}/libcrypto.a".format(self.stage_lib_dir_path))
        util.rm_file("{}/libssl.a".format(self.stage_lib_dir_path))
        sys_desc = platform.platform()
        if re.search('Linux', sys_desc) is not None \
                and re.search('x86_64', sys_desc) is not None:
            arch_arg = "linux-x86_64"
        elif re.search('Darwin', sys_desc) is not None:
            arch_arg = "darwin64-x86_64-cc"
        else:
            raise RuntimeError("could not determine platform type for openssl build options - platform is: {}".format(sys_desc))
        util.run(["./Configure",
                  "--prefix={}".format(self.cfg_obj.stage_dir),
                  "--openssldir={}".format(self.vendor_ssl_dir),
                  "--debug",
                  arch_arg,
                  # "linux-x86_64"
                  # "darwin64-x86_64-cc"
                  ],
                 self.package_clone_dir_versioned_path)

        util.run(["make", "all"], self.package_clone_dir_versioned_path)
        util.run(["make", "install"], self.package_clone_dir_versioned_path)

    def install_package(self):
        self.headers_from_stage_to_vendor("openssl", "openssl")
        self.libs_from_stage_to_vendor("libssl.*")
        self.libs_from_stage_to_vendor("libcrypto.*")

