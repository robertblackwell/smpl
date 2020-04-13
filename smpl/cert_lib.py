import sys
import json
import datetime
import os
import pprint
import shutil

import smpl.util as util 
from .package import LibraryPackage

package_name = "x509_certificate_library"
boost_release = "1.72.0"
package_url = "https://github.com/robertblackwell/x509_certificate_library.git ${release} ${clone_dir}/${package_name}"

package_targz_file = "boost_1_72_0.tar.gz"


class CertLib(LibraryPackage):
	def __init__(self, name, version, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.version = version
		self.git_url = "https://github.com/robertblackwell/x509_certificate_library.git"
		self.git_branch_arg = None
		self.package_stage_include_dir_path = os.path.join(self.defaults.stage_dir, "include", "cert")
		self.package_vendor_include_dir_path = os.path.join(self.defaults.vendor_dir, "include", "cert")
	def get_package(self):
		util.logger.writeln("CertLib get_package begin")
		super().get_package_before()

	
		# remove any old directory that is a previous git clone
		util.rm_directory(self.package_clone_dir_path)
		# util.mkdir_p(self.package_clone_dir_path)

		util.git_clone(self.git_url, self.defaults.clone_dir, self.git_branch_arg)

		# list the contents of defaults.clone_dir to demonstrate that the unpack worked
		util.list_directory(self.package_clone_dir_path)

		super().get_package_after()
		util.logger.writeln("CertLib get_package end")

	def stage_package(self):
		util.logger.writeln("Boost stage_package begin")
		super().stage_package_before()
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
		super().stage_package_after()
		util.logger.writeln("CertLib stage_package end")

	def install_package(self):
		util.logger.writeln("CertLib install_package begin")
		super().install_package_before()
		util.mkdir_p(self.vendor_lib_dir_path)
		# util.run("mkdir -p {}".format(self.vendor_lib_dir_path))

		# make sure vendor/include/cert_library exists and is empty
		util.clear_directory(self.package_vendor_include_dir_path)

		# make sure there are no cert_library in vendor/lib
		util.rm_directory_contents(self.vendor_lib_dir_path, "libcert.*")

		# util.cp_rv_fulldir(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
		util.cp_directory_contents(self.package_stage_include_dir_path, self.package_vendor_include_dir_path)

		# util.cp_rv_fulldir(self.stage_lib_dir_path,  self.vendor_lib_dir_path)
		util.cp_directory_files(self.stage_lib_dir_path, self.vendor_lib_dir_path, "libcert.*")
		super().install_package_after()
		util.logger.writeln("CertLib install_package end")

# #!/bin/bash

# function install_package {
# 	mkdir -p ${vendor}/include/cert
# 	mkdir -p ${vendor}/lib
# 	rm -rfv ${vendor}/include/cert/*
# 	rm -rfv ${vendor}/lib/libcert*
# 	cp -rv ${script_dir}/stage/include/cert/* ${vendor}/include/cert

# 	cp -rv ${script_dir}/stage/lib/libcert*.a ${vendor}/lib/
# 	echo 
# 	echo INSTALL $package complete ========================================================
# 	echo
# }

# function get_package {
# 	cd ${clone_dir}
# 	rm -rfv ${clone_dir}/${package_name}
# 	${git_clone}
# 	cd ${package_name}
# 	ls -al
# }

# function stage_package {
# 	stage_dir=${script_dir}/stage
# 	mkdir -p ${script_dir}/stage/include
# 	mkdir -p ${script_dir}/stage/lib
# 	cd ${clone_dir}/${package_name}
# 	if [ -d cmake-build-debug ] ; then 
# 		rm -rf cmake-build-debug/*
# 	else
# 		mkdir -p cmake-build-debug
# 	fi
# 	cd cmake-build-debug
# 	pwd
# 	cmake -DVENDOR_DIR=${stage_dir} -DSTAGE_DIR=${stage_dir} ..
# 	# cmake  --build . --target cert_library
# 	make -j 8 cert_library
# 	cmake --build . --target install -j 8
# }

# function verify_package_name() {
# 	if [ $project_name != "marvin++" ] ; then
# 		echo "You are in the wrong directory : [" ${project_name} "] should be at project root "
# 		exit 1
# 	fi
# }

# function help() {
# 	echo Install package ${package_name}
# 	echo Usage:
# 	echo 	install_${package_name}.sh [arg]
# 	echo
# 	echo	args is either
# 	echo		help 	Print this help message
# 	echo		install After build copy include and libs to final destination
# 	echo
# 	echo 	The required package is downloaded into a temp dir inside the scripts dir
# 	echo	If required the package is built and the headers and libs copied either
# 	echo 	to a temporary "stage" directory or to the final location		
# 	exit 0
# }

# debug=

# package_name=libcert

# if [ "$1" == "help" ] ; then help; fi


# pwd=`pwd`
# vendor=${pwd}/vendor
# project_dir=$pwd
# project_name=$(basename $project_dir)
# script_dir=$(dirname $(realpath $0))
# clone_dir=${script_dir}/cloned_repos
# git_clone="git clone https://github.com/robertblackwell/x509_certificate_library.git ${release} ${clone_dir}/${package_name}"

# echo 
# echo INSTALL $package_name begin ========================================================
# echo

# if [ "$1" == "stage" ] || [ "$1" == "install" ] || [ "$1" == "" ] ; then
# 	verify_package_name
# 	get_package
# 	stage_package
# fi

# if [ "$1" == "install" ] || [ "$1" == "install_only" ] ; then
# 	install_package
# 	echo 
# 	echo INSTALL ${package_name} complete ========================================================
# 	echo
# fi


