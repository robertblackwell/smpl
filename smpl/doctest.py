import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from smpl.defaults import Defaults

from .package import HeadersOnlyPackage

class Doctest(HeadersOnlyPackage):
	def __init__(self, name: str, parms, the_defaults: Defaults):
		super().__init__(name, the_defaults)
		self.name = name
		# the name of the directory that the cloned repo will unpack into
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "doctest")
		self.parms = parms

		# the release must match a repo tag
		self.release="2.3.7"
		self.git_url="https://github.com/onqtam/doctest.git"
		self.git_branch_arg = "{}".format(self.release)
		# the dir in the repo from where we copy headers
		self.cp_from_here_dir = os.path.join(self.package_clone_dir_path, "doctest")

	def get_package(self):
		self.get_git_repo(self.git_url, "doctest", "2.3.7")

	def stage_package(self):
		self.stage_headers_only_from_repo(repo_name = "doctest", stage_name = "doctest", repo_sub_directory = "doctest")

		# util.clear_directory(self.package_stage_include_dir_path)
		# util.cp_directory_contents(self.cp_from_here_dir, self.package_stage_include_dir_path)

	def install_package(self):
		self.headers_from_stage_to_vendor("doctest", "doctest")

		# util.clear_directory(self.package_vendor_include_dir_path)
		# util.cp_directory_contents(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
