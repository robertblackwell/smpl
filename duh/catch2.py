import sys
import json
import datetime
import os
import pprint
import shutil

import duh.util as util 
from .package import HeadersOnlyPackage


catch_release="v2.11.1"
package_description="catch_v2.11.1"
package_name="Catch2"

package_clone_stem="Catch2"
git_clone="git clone https://github.com/catchorg/Catch2.git --branch ${catch_release}"
git_url="https://github.com/catchorg/Catch2.git"
git_branch_arg = "".format(catch_release)
header_cp_pattern="single_include/catch2/*"

class Catch2(HeadersOnlyPackage):
	def __init__(self, name, version, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "Catch2")
		self.version = version
		self.catch_release="v2.11.1"
		self.git_url="https://github.com/catchorg/Catch2.git"
		self.git_branch_arg = "{}".format(self.catch_release)
		self.single_include_dir = os.path.join(self.package_clone_dir_path, "single_include")

	def get_package(self):
		# return
		# print("here")
		super().get_package_before()
		util.rm_directory("{}/{}".format(self.defaults.clone_dir, package_clone_stem))
		util.git_clone(self.git_url, self.defaults.clone_dir, self.git_branch_arg)
		# util.run(["git", "clone", "https://github.com/catchorg/Catch2.git", "--branch", "{}".format(catch_release)], where=self.defaults.clone_dir)

		super().get_package_after()
	
	def stage_package(self):
		super().stage_package_before()
		util.rm_directory(self.package_stage_include_dir_path)
		util.mkdir_p(self.package_stage_include_dir_path)

		util.cp_directory_contents(self.single_include_dir, self.package_stage_include_dir_path)

		super().stage_package_after()

	def install_package(self):
		super().install_package_before()
		util.rm_directory(self.package_vendor_include_dir_path)
		util.mkdir_p(self.package_vendor_include_dir_path)

		util.cp_directory_contents(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
		super().install_package_after()
