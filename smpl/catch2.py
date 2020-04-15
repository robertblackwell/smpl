import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from .package import HeadersOnlyPackage



class Catch2(HeadersOnlyPackage):
	def __init__(self, name, parms, the_defaults):
		package_name="Catch2"

		parms.repo_name = "Catch2"
		parms.repo_branch_argument = "v2.11.1"
		parms.stage_name = "catch2"
		parms.vendor_name = "catch2"
		parms.repo_sub_directory = "single_include/catch2"
		
		super().__init__(package_name, the_defaults)
		self.name = name
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "Catch2")
		self.parms = parms
		self.release="v2.11.1"
		self.git_url="https://github.com/catchorg/Catch2.git"
		self.git_branch_arg = self.release
		self.single_include_dir = os.path.join(self.package_clone_dir_path, "single_include")

	def get_package(self):
		self.get_git_repo(self.git_url, "Catch2", "v2.11.1")

	def stage_package(self):
		self.stage_headers_only_from_repo(repo_name = "Catch2", stage_name = "catch2", repo_sub_directory = "single_include/catch2")

	def install_package(self):
		self.headers_from_stage_to_vendor("catch2", "catch2")

		# util.clear_directory(self.package_vendor_include_dir_path)
		# util.cp_directory_contents(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
