import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from smpl.package import LibraryPackage

package_name = "boost"
boost_release = "1.72.0"
package_url = "https://dl.bintray.com/boostorg/release/{}/source/boost_1_72_0.tar.gz".format(boost_release)
package_targz_file = "boost_1_72_0.tar.gz"


class Boost(LibraryPackage):
	def __init__(self, name, parms, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.parms = parms

		self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
		self.wget_output_path = os.path.join(self.defaults.clone_dir, package_targz_file) 
		self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
		self.clone_dir_path = os.path.join(self.defaults.clone_dir, package_name + "_1_72_0")

	def get_package(self):
		self.get_and_unpack_tar(package_url, "boost_1_72_0.tar.gz", "boost_1_72_0")

	def stage_package(self):
		util.logger.writeln("Boost stage_package begin")
		util.mkdir_p(self.stage_include_dir_path)

		# make sure stage/include/boost exists and is empty 
		util.mkdir_p(self.package_stage_include_dir_path)
		util.rm_directory_contents(self.package_stage_include_dir_path)

		util.mkdir_p(self.stage_lib_dir_path)

		util.run(["rm", "-rf",  "{}/libboost*".format(self.stage_lib_dir_path)])

		util.run([
			"./bootstrap.sh", 
			"--prefix={}".format(self.defaults.stage_dir),  
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
		self.headers_from_stage_to_vendor("boost","boost")
		self.libs_from_stage_to_vendor("libboost.*")
