import sys
import json
import datetime
import os
import pprint
import shutil

import duh.util as util 
from .package import SourcePackage

package_name = "simple_buffer"

class SimpleBuffer(SourcePackage):
	def __init__(self, name, version, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.version = version
		self.git_url = "git@github.com:robertblackwell/simple_buffer.git"
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, "simple_buffer")
		self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, "src")
		self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, "simple_buffer")
	def get_package(self):
		super().get_package_before()
		util.rm_directory(self.package_clone_dir_path)
		util.git_clone(self.git_url, self.defaults.clone_dir)
		util.list_directory(self.package_clone_dir_path)
		super().get_package_after()
	
	def stage_package(self):
		super().stage_package_before()
		util.clear_directory(self.package_stage_external_src_dir_path)
		util.cp_directory_files(self.package_clone_dir_source_path, self.package_stage_external_src_dir_path, ".*")
		# util.cp_directory_files(self.package_clone_dir_path, self.package_stage_external_src_dir_path, "http_parser.c")
		util.list_directory(self.package_stage_external_src_dir_path)
	def install_package(self):
		super().install_package_before()
		util.clear_directory(self.package_external_src_dir_path)
		util.cp_directory_files(self.package_stage_external_src_dir_path,  self.package_external_src_dir_path, ".*")
		util.list_directory(self.package_external_src_dir_path)
