import os
import subprocess
import shutil
import re

class Logger:
	def __init__(self):
		self.enabled = False
		self.log_file_path = 'action_log.log'
		self.log_file = None
	def open(self):
		self.enabled = True
		self.log_file = open(self.log_file_path, "w+")
	
	def write(self, text):
		if (self.enabled):
			self.log_file.write(text)

	def writeln(self, line):
		if self.enabled:
			self.log_file.write(line + "\n")

log_file_path = ""
log_file = None

logger = Logger()
dry_run = False

# dies on error
# runs a command in array form ["cmd", "arg1", "arg2" ....]
def exec_cmd(cmd, where):
	stdout = None
	stderr = None
	reult = "123"
	if dry_run:
		return "", None
	if where is None:
		try:
			result = subprocess.run(cmd)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			s = result.returncode
			s3 = result.stderr
			s2 = result.stdout
			s2 = result.stdout
		except Exception as exception:
			print ("An error occurred while running command [{}] error type: " +type(exception).__name__ + " {}".format(cmd, str(exception)))
			quit()
	else:		
		try:
			result = subprocess.run(cmd, cwd=where) #, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			s = result.returncode
			s3 = result.stderr
			s2 = result.stdout
			s2 = result.stdout
		except Exception as exception:
			print ("An error occurred while running command [{}] error type: " +type(exception).__name__ + " {}".format(cmd, str(exception)))
			quit()

		# print("stdout: ", stdout)
		# if stderr is not None:
		# 	print("stderr: ", stderr)

def run(cmd, where=None):
	if not isinstance(cmd, list):
		raise ValueError("cmd must be array")
	if where is None:
		line = "run: [{}] ".format(cmd) 
		# print("run: [{}] ".format(cmd))
		exec_cmd(cmd, where)
		logger.writeln(line)
	else:
		line = "run: [{}] where = {} ".format(cmd, where)
		# print("run: [{}] where = {} ".format(cmd, where))
		exec_cmd(cmd, where)
		logger.writeln(line)

def set_log_file(log_file_path):
	logger.log_file_path = log_file_path
	logger.open()


def rm_file(file_path):
	if(os.path.isfile(file_path)):
		logger.writeln("remove file: {}".format(file_path))
		if not dry_run:
			os.unlink(file_path)
	else:
		logger.writeln("remove (not exist) file: {}".format(file_path))

# remove a directory and its contents if it exists
# equivalent of rm -rvf directory_path/
def rm_directory(directory_path):
	if os.path.isdir(directory_path):
		logger.writeln("rm_rfv Existing {}".format(directory_path))
		if not dry_run:
			shutil.rmtree(directory_path)
	else:
		logger.writeln("rm_rfv NonExisting {}".format(directory_path))

# remove a directory's  contents if it exists
# equivalent of rm -rvf directory_path/*
def rm_directory_contents(directory_path, pattern=".*"):
	regex = re.compile(pattern)
	if os.path.isdir(directory_path):
		logger.writeln("rm_rfv_content Existing {}".format(directory_path))
		if not dry_run:
			for root, dirs, files in os.walk(directory_path):
				for f in files:
					if regex.match(f):
						os.unlink(os.path.join(root, f))
				for d in dirs:
					shutil.rmtree(os.path.join(root, d))
	else:
		logger.writeln("rm_rfv NonExisting {}".format(directory_path))



def mkdir_p(directory_path):
	if not os.path.exists(directory_path):
		if not dry_run:
			os.makedirs(directory_path)
		logger.writeln("rm_rfv NonExisting {}".format(directory_path))
	else:
		logger.writeln("rm_rfv Existing {}".format(directory_path))

def cp_directory():
	pass

def cp_directory_fulldir(src, dest):
	if not dry_run:
		shutil.copytree(src, dest)
	logger.writeln("cp_directory_fulldir {} -> {}".format(src, dest))

def cp_directory_files(src_directory_path, dest_directory_path, pattern=".*"):
	regex = re.compile(pattern)
	if os.path.isdir(src_directory_path) and os.path.isdir(dest_directory_path):
		logger.writeln("cp_directory_files {} {} {}".format(src_directory_path, dest_directory_path, pattern))
		if not dry_run:
			for thing in os.listdir(src_directory_path):
				srcfullpath = os.path.join(src_directory_path, thing)
				destfullpath = os.path.join(dest_directory_path, thing)
				if os.path.isdir(srcfullpath):
					pass #shutil.copytree(srcfullpath, destfullpath)
				else:
					if regex.match(thing):
						shutil.copyfile(os.path.join(src_directory_path, thing), os.path.join(dest_directory_path, thing))
	else:
		raise ValueError("cp_directory_files one of the arguments is not a directory {} {}".format(src_directory_path, dest_directory_path))

def cp_directory_contents(src_directory_path, dest_directory_path, pattern=".*"):
	regex = re.compile(pattern)
	if os.path.isdir(src_directory_path) and os.path.isdir(dest_directory_path):
		logger.writeln("cp_directory_files {} {} {}".format(src_directory_path, dest_directory_path, pattern))
		if not dry_run:
			for thing in os.listdir(src_directory_path):
				srcfullpath = os.path.join(src_directory_path, thing)
				destfullpath = os.path.join(dest_directory_path, thing)
				if os.path.isdir(srcfullpath):
					shutil.copytree(srcfullpath, destfullpath)
				else:
					if regex.match(thing):
						shutil.copyfile(os.path.join(src_directory_path, thing), os.path.join(dest_directory_path, thing))
	else:
		raise ValueError("cp_directory_files one of the arguments is not a directory {} {}".format(src_directory_path, dest_directory_path))
