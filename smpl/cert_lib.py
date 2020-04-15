import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from .package import LibraryPackage

package_name = "x509_certificate_library"

class CertLib(LibraryPackage):
	def __init__(self, name, parms, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.parms = parms
		self.git_url = "https://github.com/robertblackwell/x509_certificate_library.git"
		self.git_branch_arg = None
		self.package_stage_include_dir_path = os.path.join(self.defaults.stage_dir, "include", "cert")
		self.package_vendor_include_dir_path = os.path.join(self.defaults.vendor_dir, "include", "cert")
	def get_package(self):
		self.get_git_repo(self.git_url, "x509_certificate_library")

	def stage_package(self):

		util.mkdir_p(self.stage_include_dir_path)
		util.mkdir_p(self.stage_lib_dir_path)

		util.clear_directory(self.package_stage_include_dir_path)
		util.rm_directory_contents(self.stage_lib_dir_path, "libcert.*")
		# util.run(["rm", "-rf",  "{}/libcert*".format(self.stage_lib_dir_path)])

		self.cmake_dir = os.path.join(self.package_clone_dir_path, "cmake-build-debug")
		util.clear_directory(self.cmake_dir)
		util.run([
			"cmake",
			"-DVENDOR_DIR={}".format(self.defaults.stage_dir),
			"-DSTAGE_DIR={}".format(self.defaults.stage_dir),
			".."
		], self.cmake_dir)
		util.run([
			"make",
			"-j30",
			"cert_library"
		], self.cmake_dir)
		util.run([
			"cmake", 
			"--build", 
			".",  
			"--target",
			"install",
			"-j", "8"
		], self.cmake_dir)
		# just installed the headers into stage/include/cert
		util.logger.writeln("CertLib stage_package end")

	def install_package(self):
		self.headers_from_stage_to_vendor("cert","cert")
		self.libs_from_stage_to_vendor("libcert.*")

		# util.logger.writeln("CertLib install_package begin")
		# super().install_package_before()
		# util.mkdir_p(self.vendor_lib_dir_path)
		# # util.run("mkdir -p {}".format(self.vendor_lib_dir_path))

		# # make sure vendor/include/cert_library exists and is empty
		# util.clear_directory(self.package_vendor_include_dir_path)

		# # make sure there are no cert_library in vendor/lib
		# util.rm_directory_contents(self.vendor_lib_dir_path, "libcert.*")

		# # util.cp_rv_fulldir(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
		# util.cp_directory_contents(self.package_stage_include_dir_path, self.package_vendor_include_dir_path)

		# # util.cp_rv_fulldir(self.stage_lib_dir_path,  self.vendor_lib_dir_path)
		# util.cp_directory_files(self.stage_lib_dir_path, self.vendor_lib_dir_path, "libcert.*")
		# super().install_package_after()
		# util.logger.writeln("CertLib install_package end")

