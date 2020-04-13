import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from .package import HeadersOnlyPackage


debug=None
package_name="json"
package_clone_stem="json"
package_description="nlohman_json_${json_release}"
git_clone="git clone https://github.com/nlohmann/json.git"
header_cp_pattern="single_include/nlohmann/json.hpp"


class NLohmannJson(HeadersOnlyPackage):
	def __init__(self, name, version, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "json")
		self.version = version
		self.git_url="https://github.com/nlohmann/json.git"
		self.git_branch_arg = None
		self.single_include_dir = os.path.join(self.package_clone_dir_path, "single_include", "nlohmann")
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "json")
		self.package_stage_include_dir_path = os.path.join(self.defaults.stage_dir, "include", "json")
		self.package_vendor_include_dir_path = os.path.join(self.defaults.vendor_dir, "include", "json")

	def get_package(self):
		util.rm_directory(self.package_clone_dir_path)
		util.git_clone(self.git_url, self.defaults.clone_dir, self.git_branch_arg)
		util.list_directory(self.package_clone_dir_path)
	
	def stage_package(self):
		util.clear_directory(self.package_stage_include_dir_path)
		util.cp_directory_contents(self.single_include_dir, self.package_stage_include_dir_path)

	def install_package(self):
		util.clear_directory(self.package_vendor_include_dir_path)
		util.cp_directory_contents(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
