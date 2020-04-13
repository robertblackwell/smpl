import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from .package import SourcePackage

package_name = "cxxurl"


class CxxUrl(SourcePackage):
	def __init__(self, name, version, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.version = version
		self.git_url = "git@github.com:robertblackwell/cxxurl.git"
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "cxxurl")
		self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "cxxurl")
		self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "cxxurl")
	def get_package(self):
		util.rm_directory(self.package_clone_dir_path)
		util.git_clone(self.git_url, self.defaults.clone_dir)
		util.list_directory(self.package_clone_dir_path)
	
	def stage_package(self):
		util.clear_directory(self.package_stage_external_src_dir_path)
		util.cp_directory_files(self.package_clone_dir_path, self.package_stage_external_src_dir_path, "url.*")
		util.list_directory(self.package_stage_external_src_dir_path)

	def install_package(self):
		util.clear_directory(self.package_external_src_dir_path)
		util.cp_directory_files(self.package_stage_external_src_dir_path,  self.package_external_src_dir_path, ".*")
		util.list_directory(self.package_external_src_dir_path)