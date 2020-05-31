import os
import subprocess
import shutil
import re
import pprint
from typing import Union, TextIO, List, AnyStr


class Logger:
    def __init__(self):
        self.enabled: bool = False
        self.log_file_path: str = 'action_log.log'
        self.log_file = None

    def open(self) -> None:
        self.enabled = True
        self.log_file: TextIO = open(self.log_file_path, "w+")

    def write(self, text: str) -> None:
        if self.enabled:
            self.log_file.write(text)

    def writeln(self, line: str) -> None:
        if self.enabled:
            self.log_file.write(line + "\n")


log_file_path = ""
log_file = None

logger: Logger = Logger()
dry_run: bool = False


def try_popen(cmd, where: str):
    print("in try_popen")
    popen = subprocess.Popen(cmd, cwd=where, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code: int = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


# dies on error
# runs a command in array form ["cmd", "arg1", "arg2" ....]
def exec_cmd(cmd, where: str):
    stdout = None
    stderr = None
    reult = "123"
    if dry_run:
        return "", None
    if where is None:
        try:
            result = subprocess.run(cmd)  # stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s = result.returncode
            s3 = result.stderr
            s2 = result.stdout
            s2 = result.stdout
        except Exception as exception:
            print("Cmd was ")
            pprint(cmd)
            print("XXAn error occurred while running command [{}] error type: " + type(exception).__name__ + " {}".format(
                ",".join(cmd), str(exception)))
            quit()
    else:
        try:
            result = subprocess.run(cmd, cwd=where)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s = result.returncode
            s3 = result.stderr
            s2 = result.stdout
            s2 = result.stdout
        except Exception as exception:
            print("Cmd was ")
            pprint(cmd)
            print("XXAn error occurred while running command [{}] error type: " + type(exception).__name__ + " {}".format(
                ",".join(cmd), str(exception)))
            quit()

    # print("stdout: ", stdout)
    # if stderr is not None:
    # 	print("stderr: ", stderr)


def run(cmd, where: Union[str, None] = None) -> None:
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


def set_log_file(logfile_path):
    logger.log_file_path = logfile_path
    logger.open()


# ensures that a directory exists and is empty
def clear_directory(directory_path: str) -> None:
    rm_directory(directory_path)
    mkdir_p(directory_path)


def list_directory(directory_path: str) -> None:
    exec_cmd(["ls", "-al"], where=directory_path)


#
# Clones a github repo, optionally with a --branch argument, 
# command is performed with the specified directory as the working directory.
#  This ensures that the cloned repo is named the same as the repo and located in the
# specified working directory
# 
# @param string git_url 			In the form git@github:<username>/reponame.git 
# 									or https://github.com/<username>/reportname
# @param string where 				The desired working directory.
# @param string|None git_branch_arg An argument for the git clone --branch option. Specifies which tag/branch to clone
# 
# @return Nothing
# 
def git_clone(git_url: str, cwd_where: str, git_branch_arg: Union[str, None] = None) -> None:
    logger.writeln("/usr/bin/git clone: {} {} into cwd {}".format(git_url, git_branch_arg, cwd_where))
    if git_branch_arg is None:
        exec_cmd(["/usr/bin/git", "clone", git_url], where=cwd_where)
    else:
        exec_cmd(["/usr/bin/git", "clone", git_url, "--branch", git_branch_arg], where=cwd_where)


def rm_file(file_path: AnyStr) -> None:
    if os.path.isfile(file_path):
        logger.writeln("remove file: {}".format(file_path))
        if not dry_run:
            os.unlink(file_path)
    else:
        logger.writeln("remove (not exist) file: {}".format(file_path))


# remove a directory and its contents if it exists
# equivalent of rm -rvf directory_path/
def rm_directory(directory_path: AnyStr) -> None:
    if os.path.isdir(directory_path):
        logger.writeln("rm_rfv Existing {}".format(directory_path))
        if not dry_run:
            print("cll rmtree on", directory_path)
            shutil.rmtree(directory_path)
    else:
        logger.writeln("rm_rfv NonExisting {}".format(directory_path))


# remove a directory's  contents if it exists
# equivalent of rm -rvf directory_path/*
def rm_directory_contents(directory_path: AnyStr, pattern: str = ".*") -> None:
    regex = re.compile(pattern)
    if os.path.isdir(directory_path):
        logger.writeln("rm_rfv_content Existing {}".format(directory_path))
        if not dry_run:
            for root, dirs, files in os.walk(directory_path):
                for f in files:
                    if regex.match(f):
                        os.unlink(os.path.join(root, f))
                for d in dirs:
                    print ("cll rmtree on", root, " ", d)
                    if os.path.islink(os.path.join(root, d)):
                        os.unlink(os.path.join(root,d))
                    else:
                        shutil.rmtree(os.path.join(root, d))
    else:
        logger.writeln("rm_rfv NonExisting {}".format(directory_path))


def mkdir_p(directory_path: AnyStr) -> None:
    if not os.path.exists(directory_path):
        if not dry_run:
            os.makedirs(directory_path)
        logger.writeln("rm_rfv NonExisting {}".format(directory_path))
    else:
        logger.writeln("rm_rfv Existing {}".format(directory_path))


def cp_directory():
    pass


def cp_directory_fulldir(src: AnyStr, dest: AnyStr) -> None:
    if not dry_run:
        shutil.copytree(src, dest)
    logger.writeln("cp_directory_fulldir {} -> {}".format(src, dest))


#
# copy all the files from the src_directory_path that match the given regex patter
# to the dest_directory_path. Does NOT recurse into sub-directories
#  @param string src_directory_path
#  @param string dest_directory_path
#  @param string pattern default=".*" is a regex patter
# 
def cp_directory_files(src_directory_path: str, dest_directory_path: str, pattern=".*") -> None:
    regex = re.compile(pattern)
    if os.path.isdir(src_directory_path) and os.path.isdir(dest_directory_path):
        logger.writeln("cp_directory_files {} {} {}".format(src_directory_path, dest_directory_path, pattern))
        if not dry_run:
            for thing in os.listdir(src_directory_path):
                srcfullpath = os.path.join(src_directory_path, thing)
                destfullpath = os.path.join(dest_directory_path, thing)
                if os.path.isdir(srcfullpath):
                    pass  # shutil.copytree(srcfullpath, destfullpath)
                else:
                    if regex.match(thing):
                        shutil.copyfile(os.path.join(src_directory_path, thing),
                                        os.path.join(dest_directory_path, thing))
    else:
        raise ValueError("cp_directory_files one of the arguments is not a directory {} {}".format(src_directory_path,
                                                                                                   dest_directory_path))


#
# copy the contents of the src_directory_path 
# to the dest_directory_path. DOES recurse into sub-directories.
# Unlike shutil.copytree the dest_subdirectory must already exist.
# prior to calling this function.
# 
# @param string src_directory_path
# @param string dest_directory_path  
# @param string pattern 			Ignored
# @return nothing
# @throw ValueError if the inputs are not valid existing directory paths
# 
def cp_directory_contents(src_directory_path: str, dest_directory_path: str, pattern=".*") -> None:
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
                        shutil.copyfile(os.path.join(src_directory_path, thing),
                                        os.path.join(dest_directory_path, thing))
    else:
        raise ValueError("cp_directory_files one of the arguments is not a directory {} {}".format(src_directory_path,
                                                                                                   dest_directory_path))
