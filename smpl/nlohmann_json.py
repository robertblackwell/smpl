import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from .package import HeadersOnlyPackage


package_name="json"

class NLohmannJson(HeadersOnlyPackage):
	def __init__(self, name, parms, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "json")
		self.parms = parms
		self.git_url="https://github.com/nlohmann/json.git"
		self.git_branch_arg = None
		self.single_include_dir = os.path.join(self.package_clone_dir_path, "single_include", "nlohmann")
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "json")
		self.package_stage_include_dir_path = os.path.join(self.defaults.stage_dir, "include", "json")
		self.package_vendor_include_dir_path = os.path.join(self.defaults.vendor_dir, "include", "json")

	def get_package(self):
		self.get_git_repo(self.git_url, "json", self.git_branch_arg)
	
	def stage_package(self):
		self.stage_headers_only_from_repo(repo_name = "json", stage_name = "json", repo_sub_directory = "single_include/nlohmann")

		# util.clear_directory(self.package_stage_include_dir_path)
		# util.cp_directory_contents(self.single_include_dir, self.package_stage_include_dir_path)

	def install_package(self):
		self.headers_from_stage_to_vendor("json", "json")

		# util.clear_directory(self.package_vendor_include_dir_path)
		# util.cp_directory_contents(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
