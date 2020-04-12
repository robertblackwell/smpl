import sys
import json
import datetime
import os
import pprint
import shutil

import duh.util as util 
from .package import LibraryPackage

package_name = "openssl"
openssl_name = "openssl-1.1.1f"

# package_url = "https://dl.bintray.com/boostorg/release/{}/source/boost_1_72_0.tar.gz".format(boost_release)
package_url = "https://www.openssl.org/source/{}.tar.gz".format(openssl_name)
package_targz_file = "tar xvzf {}.tar.gz".format(openssl_name)


class OpenSSL(LibraryPackage):
	def __init__(self, name, version, the_defaults):
		super().__init__(package_name, the_defaults)
		self.name = name
		self.version = version

		self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
		self.wget_output_path = self.defaults.clone_dir
		self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
		self.vendor_ssl_dir = os.path.join(self.defaults.vendor_dir, "ssl")
		self.package_clone_dir_versioned_path = os.path.join(self.defaults.clone_dir, "openssl-1.1.1f")

	def get_package(self):
		super().get_package_before()
		util.rm_file(self.package_targz_file_path)
		util.rm_directory(self.package_clone_dir_path)
		util.run(["wget", "-O", self.package_targz_file_path, package_url])

		# unpack the tar file cd to the clone_dir before unpacking
		# this will result in a new dir inside clone_dir with a name line boost_1_72.2
		util.run(["tar", "-xvzf", self.package_targz_file_path, "-C", self.defaults.clone_dir])

		# run("wget -O {} {}".format(self.wget_output_path, package_url))
		# run("tar xvzf {} -C {}".format(self.package_targz_file_path, self.package_clone_dir_path))
		# run("ls -al {}".format(self.package_clone_dir_path))
		util.list_directory(self.package_clone_dir_versioned_path)
		super().get_package_after()
	
	def stage_package(self):
		util.clear_directory(self.package_stage_include_dir_path)
		util.rm_file("{}/libcrypto.a".format(self.stage_lib_dir_path))
		util.rm_file("{}/libssl.a".format(self.stage_lib_dir_path))

		util.run(["./Configure",
			"--prefix={}".format(self.defaults.stage_dir),
			"--openssldir={}".format(self.vendor_ssl_dir), 
			"--debug",
			"linux-x86_64"
			# "darwin64-x86_64-cc"
		],
		self.package_clone_dir_versioned_path)

		util.run(["make", "all"], self.package_clone_dir_versioned_path)
		util.run(["make", "install"], self.package_clone_dir_versioned_path)
		super().stage_package_after()

	def install_package(self):
		super().install_package_before()
		util.clear_directory(self.package_vendor_include_dir_path)
		util.run(["rm", "-rf", "{}/libcrypto*".format(self.vendor_lib_dir_path)])
		util.run(["rm", "-rf", "{}/libssl*".format(self.vendor_lib_dir_path)])

		util.cp_directory_contents(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
		util.cp_directory_files(self.stage_lib_dir_path,  self.vendor_lib_dir_path, "lib.*")

		# util.cp_rv_fulldir(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
		util.cp_directory_contents(self.package_stage_include_dir_path, self.package_vendor_include_dir_path)
		util.cp_directory_files(self.stage_lib_dir_path, self.vendor_lib_dir_path, "libcrypto.*")
		util.cp_directory_files(self.stage_lib_dir_path, self.vendor_lib_dir_path, "libcrypto.*")

		super().install_package_after()

	# 	self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
	# 	self.wget_output_path = os.path.join(self.defaults.clone_dir, package_targz_file) 
	# 	self.package_targz_file_path = os.path.join(self.defaults.clone_dir, package_targz_file)
	# 	self.clone_dir_path = os.path.join(self.defaults.clone_dir, package_name + "_1_72_0")

	# def get_package(self):
	# 	return
	# 	print("here")
	# 	util.logger.writeln("Boost get_package begin")
	# 	super().get_package_before()

	# 	# remove any old tar file
	# 	util.rm_file(self.package_targz_file_path)
		
	# 	# remove any old directory that is a previous unpacked tar
	# 	util.rm_directory(self.package_clone_dir_path)

	# 	# download the new tar file
	# 	util.run(["wget", "-O", self.package_targz_file_path, package_url])

	# 	# unpack the tar file cd to the clone_dir before unpacking
	# 	# this will result in a new dir inside clone_dir with a name line boost_1_72.2
	# 	util.run(["tar", "-xvzf", self.package_targz_file_path, "-C", self.defaults.clone_dir])

	# 	# list the contents of defaults.clone_dir to demonstrate that the unpack worked
	# 	util.run(["ls", "-al", self.defaults.clone_dir])

	# 	super().get_package_after()
	# 	util.logger.writeln("Boost get_package end")

	# def stage_package(self):
	# 	return
	# 	util.logger.writeln("Boost stage_package begin")
	# 	super().stage_package_before()
	# 	util.mkdir_p(self.stage_include_dir_path)

	# 	# make sure stage/include/boost exists and is empty 
	# 	util.mkdir_p(self.package_stage_include_dir_path)
	# 	util.rm_directory_contents(self.package_stage_include_dir_path)

	# 	util.mkdir_p(self.stage_lib_dir_path)

	# 	util.run(["rm", "-rf",  "{}/libboost*".format(self.stage_lib_dir_path)])

	# 	util.run([
	# 		"./bootstrap.sh", 
	# 		"--prefix={}".format(self.defaults.stage_dir),  
	# 		"darwin64-x86_64-cc"
	# 	], self.clone_dir_path)
	# 	util.run([
	# 		"./b2",
	# 		"install",
	# 		"--link=static",
	# 		"--threading=multi",
	# 		"--variant=debug",
	# 		"--layout=system",
	# 	], self.clone_dir_path)
	# 	super().stage_package_after()
	# 	util.logger.writeln("Boost stage_package end")

	# def install_package(self):
	# 	util.logger.writeln("Boost install_package begin")
	# 	super().install_package_before()
	# 	util.mkdir_p(self.vendor_lib_dir_path)
	# 	# util.run("mkdir -p {}".format(self.vendor_lib_dir_path))

	# 	# make sure vendor/include/boost exists and is empty
	# 	util.mkdir_p(self.package_vendor_include_dir_path)
	# 	util.rm_directory_contents(self.package_vendor_include_dir_path)

	# 	# make sure there are no libboost* libraries in vendor/lib
	# 	util.rm_directory_contents(self.vendor_lib_dir_path, "libboost.*")

	# 	# util.cp_rv_fulldir(self.package_stage_include_dir_path,  self.package_vendor_include_dir_path)
	# 	util.cp_directory_contents(self.package_stage_include_dir_path, self.package_vendor_include_dir_path)

	# 	# util.cp_rv_fulldir(self.stage_lib_dir_path,  self.vendor_lib_dir_path)
	# 	util.cp_directory_files(self.stage_lib_dir_path, self.vendor_lib_dir_path, "libboost.*")
	# 	super().install_package_after()
	# 	util.logger.writeln("Boost install_package end")
