import sys
import json
import datetime
import pprint
import os

import smpl.util as util 

# """
# PackageBase
# ===========
# 
# Each installable package is represented by a class (for example the Boost and Catch2 classes)
# 
# The process of installing a packages includes a lot of behavior that is either common across all
# packages (or at least all packages of the same 'type') or can easily be achieved by paramterizing
# shared functions. Such common functions or behavoir are provided to the end package classes
# by an inheritance chain consisting of three layers
# 
# -	PackageBase - is the lowest level of the inheritence chain and is common to all packages
# 
# -	at the next level there are three classes that represent the 3 types of c/c++ packages that
# 	this project can install:
# 
# 	-	LibraryPackage 		- represents a traditional c/c++ headers+library package.
# 	-	HeadersOnlyPackage 	- represents a c/c++ package that is delivered entirely as header files
# 	-	SourcePackage 		- a c/c++ package that is delivered as headers and source files that must be compiled 
# 							by the hosting project
# 
# 	see the class for each type for more details  
# 
# """
class PackageBase(object):
	def __init__(self, package_name, the_defaults):
		self.defaults = the_defaults
		self.package_name = package_name
		self.package_clone_dir_path = os.path.join(self.defaults.clone_dir, package_name)
		self.stage_include_dir_path = os.path.join(self.defaults.script_dir, "stage", "include")
		self.stage_lib_dir_path = os.path.join(self.defaults.script_dir, "stage", "lib")
		self.vendor_include_dir_path = os.path.join(self.defaults.vendor_dir, "include")
		self.vendor_lib_dir_path = os.path.join(self.defaults.vendor_dir, "lib")

		self.package_stage_include_dir_path = os.path.join(self.stage_include_dir_path, package_name)
		self.package_vendor_include_dir_path = os.path.join(self.vendor_include_dir_path, package_name)
	
	# """
	# repo_url: 	is something like git@github.com:robertblackwell/x509_certificate_library
	# 				or fil:///home/robert/git-repos/x509_certificate_library
	# 
	# repo_name: 	is the x509_certificate_library part of the url. Passed separately so that this
	# 				function knows the name of the directory created by a git clone command
	# 
	# branch_argument: allows the cloning of a spcecific branch or tag.	
	# """
	def get_git_repo(self, repo_url: str, repo_name: str, branch_argument=None):

		package_clone_dir = os.path.join(self.defaults.clone_dir, repo_name)
		util.rm_directory(package_clone_dir)
		util.git_clone(self.git_url, self.defaults.clone_dir, branch_argument)
		util.list_directory(package_clone_dir)

	def get_and_unpack_tar(self, tar_url, tar_file_name, tar_unpacked_name):
		package_clone_dir = os.path.join(self.defaults.clone_dir, tar_unpacked_name)
		util.rm_directory(package_clone_dir)
		tar_file_path = os.path.join(self.defaults.clone_dir, tar_file_name)
		util.rm_file(tar_file_path)
		util.run(["wget", "-O", tar_file_path, tar_url])
		util.run(["tar", "-xvzf", tar_file_path, "-C", self.defaults.clone_dir])
		util.list_directory(self.defaults.clone_dir)
		util.list_directory(package_clone_dir)

	def headers_from_stage_to_vendor(self, stage_name, vendor_name):
		"""
		Empties vendor/include/vendor_name
		and then
		Copies header files from stage/include/stage_name to vendor/include/vendor_name
		"""
		from_dir = os.path.join(self.stage_include_dir_path, stage_name)
		to_dir = os.path.join(self.vendor_include_dir_path, vendor_name)
		util.clear_directory(to_dir)
		util.cp_directory_contents(from_dir, to_dir)

	def libs_from_stage_to_vendor(self, lib_pattern):
		"""
		Removes all files matching lib_pattern from vendor/lib
		and then
		copies lib files matching lib_patterm from from stage/lib to vendor/lib
		"""
		from_dir = self.stage_lib_dir_path
		to_dir = self.vendor_lib_dir_path
		util.rm_directory_contents(to_dir, lib_pattern)
		util.cp_directory_files(from_dir, to_dir, lib_pattern)
		util.list_directory(to_dir)

# """
# 
# LibraryPackage
# ===============
# 
# This class is the base for package specific classes where the package is of a type that delivers
# both header files and compiled/linked libraries to its hosting project. The installation of such
# a package requires broadley three steps:
# 
# 	1.	Get the package. This means either cloning a git repo into a common location called the 'clone'
# 		directory or downloading (eg with wget) a 'tar' file into the clone directory and then unpacking
# 		that tar in the clone directory. In either case the result
# 		is a 'source' version of the package as a sub-dir of the clone dir.
# 
# 		In addition there is some house keeping to do in this step. Make sure the clone directory exists
# 		before starting the process and making sure tha previous 'tar' files and unpacked directories
# 		do not exist, as this might cause a new download and unpack to fail.
# 
# 	2.	Build the package and install its deliverables into a location called the 'stage' directory.
# 		The build and install steps at very often unqiue to the package, as for example in the case of
# 		the 'boost' or 'openssl' libraries. However the result of this step is that 
# 
# 		-	the header files for such a package end up in <stag_dir>/include/<package_name>, eg
# 			all boost headers end up in <stage_dir_path>/include/boost
# 
# 		-	and all library files built for the package end up in <stage_dir_path/lib>
# 
# 		Again there are some housekeeping chores. Make sure the 'stage' directory exists,
# 		that <stage_dir_path>/include/<packge_name> is empty.
# 
# 		Make sure that there are no 'old' libraries from previous installs of this package in <stage_dir_path>/lib
# 		by deleting all files in <stage_dir_path>/lib that match a pattern unique to this package.
# 
# 	3.	The final step is transferring headers and libraries from the 'stage' directory to their final home
# 		inside the hosting project. This utility assumes that the final location is common to all packages
# 		of this type and that location is called the 'vendor' directory and is typically named
# 
# 		<project_root_dir>/vendor.
# 
# 		Copy all package headers from <stage_dir_path>/include/<package_name> to <vendor_dir_path>/include/<package_name>
# 
# 		Copy all package library files from <stage_dir_path>/lib to <vendor_dir_path>/lib
# 
# 		Again there is some house keeping. Make sure that the vendor include and lib directories exist.
# 		Make sure that <vendor_dir_path>/include/<package_name> is empty at the start of this copy and
# 		that all 'old' or residual library files from previous installs of this package have been deleted
# 		from vendor/lib.
# """
class LibraryPackage(PackageBase):

	def __init__(self, package_name, the_defaults):
		super().__init__(package_name, the_defaults)

# """
# 
# HeadersOnlyPackage
# ====================
# 
# Header only packages are common in the c++ world. Many of the boost libraries are such 
# as are Catch2 and doctest well known unit testing frameworks.
# The process of installing HO packages follow the same three steps as LibraryPackages,
# however there is no genuine 'build'.
# 
# 1.	Get the package is the same as for a LibraryPackage except cloning from a git repo
# 		is more common that 'tar' file download and unpack.
# 
# 2. 	Staging is simply a matter of coping the necessary headers files from the packages clone directory
# 		into <stage_dir>/include/<package_name>.
# 
# 		The only little wrinkle is that the location of the required header files in the downloaded/cloned
# 		package clone directory can vary and requires a custom specification for each package.
# 
# 3.  	Final installation follows exactly the same process as the installation of the header files
# 		for a LibraryPackage.
# 
# """
class HeadersOnlyPackage(PackageBase):
	def __init__(self, package_name, the_defaults):
		super().__init__(package_name, the_defaults)
		print("HeaderOnlyPackage")
	
	# """
	# copy the header files for a headers only package from their location in the clone
	# directory into the stage/include/package_name directory
	#	 
	# repo_name: is the name of the sub-dir of clone_dir that holds the repo
	# stage_name: the subdir of stage/include where the headers are to go
	# pattern: a regex pattern selecting only some headers files
	# repo_sub_directory: in some cases the required headers are in a sub-dir of the repo directory
	# 
	# """
	def stage_headers_only_from_repo(self, repo_name, stage_name, repo_sub_directory=None):
		to_dir = os.path.join(self.stage_include_dir_path, stage_name)
		if (repo_sub_directory is None):
			from_dir = os.path.join(self.defaults.clone_dir, repo_name)
		else:
			from_dir = os.path.join(self.defaults.clone_dir, repo_name, repo_sub_directory)
		util.clear_directory(to_dir)
		util.cp_directory_contents(from_dir, to_dir)
		util.list_directory(to_dir)


# """
# 
# SourcePackage
# ===============
# 
# Some (typically small) packages are only available as true source, that is header (.h or .hpp) files and
# true source (.cpp or .c) files and must be compiled into object files and linked with the hosting project
# by the hosting project build system. Again the process of installing such a package follows three steps.
# 
# 1. get the package. Same as the previous two classes.
# 
# 2. 	Stage the package. Copy the required source (.c/.cpp) files and required header files (.h/.hpp) from
# 		where ever they are located in the packages clone dir into a special location in the stage directory.
# 		That special location in called <stage_dir>/external/<package_name>.
# 
# 		The wrinkle in this step is what source and header files and where are they located in the cloned/unpacked
# 		directory. This will typically require a few lines of custom code for such a package.
# 
# 3.	Final install. This utility currently installs such a package by copying all source and headers from:
# 
# 		<stage_dir>/external/<package_name> to <project_dir>/<project_source_dir>/external_src/<package_name>
# 
# 		The host project must ensure that all the source files in 
# 
# 		<project_dir>/<project_source_dir>/external_src/
# 
# 		are compiled and included in the relevant link steps by the host projects build system.
# 
# """
class SourcePackage(PackageBase):
	def __init__(self, package_name, the_defaults):
		super().__init__(package_name, the_defaults)
		print("SourcePackage")
		self.stage_external_src_dir_path = os.path.join(self.defaults.stage_dir,"external_src")
		self.package_stage_external_src_dir_path = os.path.join(self.stage_external_src_dir_path, self.package_name)
		self.package_external_src_dir_path = os.path.join(self.defaults.source_dir, "external_src", self.package_name)
		self.project_external_src_dir_path = self.defaults.external_dir
	# 
	# copy the header and source files for a source package from their location in the clone
	# directory into the stage/external/package_name directory
	#	 
	# repo_name: is the name of the sub-dir of clone_dir that holds the repo
	# stage_name: the subdir of stage/external where the headers+source are to go
	# pattern: a regex pattern selecting only some headers+source files
	# repo_sub_directory: in some cases the required headers+source are in a sub-dir of the repo directory
	# 
	def stage_source(self, repo_name, stage_name, repo_sub_directory=None):

		to_dir = os.path.join(self.stage_external_src_dir_path, stage_name)
		if (repo_sub_directory is None):
			from_dir = os.path.join(self.defaults.clone_dir, repo_name)
		else:
			from_dir = os.path.join(self.defaults.clone_dir, repo_name, repo_sub_directory)
		util.clear_directory(to_dir)
		util.cp_directory_contents(from_dir, to_dir)
		util.list_directory(to_dir)

	def install_stage_to_project(self, stage_name, source_name):
		"""
		Empties project_source/external_src/source_name
		and then
		Copies header+source files from stage/external/stage_name to project_sourcer/external_src/source_name
		"""
		from_dir = os.path.join(self.stage_external_src_dir_path, stage_name)
		to_dir = os.path.join(self.project_external_src_dir_path, source_name)
		util.clear_directory(to_dir)
		util.cp_directory_contents(from_dir, to_dir)
		util.list_directory(to_dir)


