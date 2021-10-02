import os
from smpl.package import SourcePackage
from smpl.config_file import ConfigObject, PackageParms
import smpl.log_module as logger

class UriParser(SourcePackage):
	def __init__(self, name, parms: PackageParms, cfg_obj: ConfigObject):
		self.package_name = "urlparser"
		super().__init__(name, cfg_obj)
		self.name = name
		self.parms = parms
		self.package_git_name = "urlparser"
		self.release = ""
		self.git_url = "https://github.com/robertblackwell/{}.git".format(self.package_git_name)
		self.package_clone_dir_path = os.path.join(self.cfg_obj.clone_dir, self.package_git_name)
		self.package_clone_dir_source_path = os.path.join(self.package_clone_dir_path, self.package_stage_include_dir_path)
		self.package_stage_source_path = os.path.join(self.package_stage_external_src_dir_path, self.package_stage_include_dir_path)

	def get_package(self):
		logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
		self.get_git_repo(self.git_url, "urlparser")
	
	def stage_package(self):
		logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
		self.stage_source("urlparser", "urlparser")

	def install_package(self):
		logger.debugln("class: {} package name {} ".format(type(self).__name__, self.name))
		self.install_stage_to_project("urlparser" , "uri-parser")
