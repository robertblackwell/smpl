import os
import smpl.util as util
from .package import LibraryPackage

package_name = "openssl"
openssl_name = "openssl-1.1.1f"

# package_url = "https://dl.bintray.com/boostorg/release/{}/source/boost_1_72_0.tar.gz".format(boost_release)
package_url = "https://www.openssl.org/source/{}.tar.gz".format(openssl_name)
package_targz_file = "tar xvzf {}.tar.gz".format(openssl_name)


class OpenSSL(LibraryPackage):
    def __init__(self, name, parms, the_defaults):
        super().__init__(package_name, the_defaults)
        self.name = name
        self.parms = parms
        self.release = "1.1.1f"
        self.package_url = "https://www.openssl.org/source/{}.tar.gz".format(openssl_name)

        self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
        self.wget_output_path = self.defaults.clone_dir
        self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
        self.vendor_ssl_dir = os.path.join(self.defaults.vendor_dir, "ssl")
        self.package_clone_dir_versioned_path = os.path.join(self.defaults.clone_dir, "openssl-1.1.1f")

    def get_package(self):
        self.get_and_unpack_tar(package_url, package_targz_file, openssl_name)

    def stage_package(self):
        util.clear_directory(self.package_stage_include_dir_path)
        util.rm_file("{}/libcrypto.a".format(self.stage_lib_dir_path))
        util.rm_file("{}/libssl.a".format(self.stage_lib_dir_path))

        util.run(["./Configure",
                  "--prefix={}".format(self.defaults.stage_dir),
                  "--openssldir={}".format(self.vendor_ssl_dir),
                  "--debug",
                  "linux-x86_64"
                  # "darwin64-x86_64-cc"
                  ],
                 self.package_clone_dir_versioned_path)

        util.run(["make", "all"], self.package_clone_dir_versioned_path)
        util.run(["make", "install"], self.package_clone_dir_versioned_path)

    def install_package(self):
        self.headers_from_stage_to_vendor("openssl", "openssl")
        self.libs_from_stage_to_vendor("libssl.*")
        self.libs_from_stage_to_vendor("libcrypto.*")

