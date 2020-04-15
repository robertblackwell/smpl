import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from smpl.package import SourcePackage


class UriParser(SourcePackage):
	def __init__(self, name, parms, the_defaults):
		self.package_name = "urlparser"
		super().__init__(self.package_name, the_defaults)
		self.name = name
		self.parms = parms
		self.package_git_name = "urlparser"
		self.git_url = "git@github.com:robertblackwell/{}.git".format(self.package_git_name)
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, self.package_git_name)
		self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, self.package_stage_include_dir_path)
		self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, self.package_stage_include_dir_path)

	def get_package(self):
		self.get_git_repo(self.git_url, "urlparser")
	
	def stage_package(self):
		self.stage_source("urlparser", "urlparser")
		# util.clear_directory(self.package_stage_external_src_dir_path)
		# util.cp_directory_files(self.package_clone_dir_path, self.package_stage_external_src_dir_path, "Uri.*")
		# util.list_directory(self.package_stage_external_src_dir_path)

	def install_package(self):
		self.install_stage_to_project("urlparser" , "urlparser")
		# util.clear_directory(self.package_external_src_dir_path)
		# util.cp_directory_files(self.package_stage_external_src_dir_path,  self.package_external_src_dir_path, ".*")
		# util.list_directory(self.package_external_src_dir_path)
