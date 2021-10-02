import os
import shutil
import re
from typing import Union, TextIO, List, AnyStr
import smpl.exec as exec
import smpl.log_module as logger

dry_run = False
# 
# Configure util for a dry_run - be sure to pass this on to exec module
# as well
# 
def configure(dryrun):
    dry_run = dryrun
    exec.configure(arg_dry_run=dry_run)

# get a remote file
def wget(url, desf_file_name):
    exec.run(["wget", "-q", "-O", desf_file_name, url])


# ensures that a directory exists and is empty
def clear_directory(directory_path: str) -> None:
    logger.debugln(" directory_path: {}".format(directory_path))
    rm_directory(directory_path)
    mkdir_p(directory_path)

# list the contents of a directory
def list_directory(directory_path: str) -> None:
    logger.debugln(" directory_path: {}".format(directory_path))
    if os.path.isdir(directory_path):
        exec.exec_cmd(["ls", "-al"], where=directory_path)
    else:
        raise RuntimeError("Invalid directory path " + directory_path)


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
    logger.debugln(" url: {} branch: {} into cwd {}".format(git_url, git_branch_arg, cwd_where))
    if git_branch_arg is None:
        exec.run(["/usr/bin/git", "clone", git_url], where=cwd_where)
    else:
        exec.run(["/usr/bin/git", "clone", git_url, "--branch", git_branch_arg], where=cwd_where)

# remove a file
def rm_file(file_path: AnyStr) -> None:
    logger.debugln(" file_path: {}".format(file_path))
    if os.path.isfile(file_path):
        logger.debugln(" {}".format(file_path))
        if not dry_run:
            os.unlink(file_path)
    else:
        logger.debugln(" not exist: {}".format(file_path))


# remove a directory and its contents if it exists
# equivalent of rm -rvf directory_path/
def rm_directory(directory_path: AnyStr) -> None:
    logger.debugln(" directory_path: {}".format(directory_path))
    if os.path.isdir(directory_path):
        logger.debugln(" Existing {}".format(directory_path))
        if not dry_run:
            logger.debugln(" call rmtree on {}".format(directory_path))
            shutil.rmtree(directory_path)
    else:
        logger.debugln(" NonExisting {}".format(directory_path))


# remove a directory's  contents if it exists
# equivalent of rm -rvf directory_path/*
def rm_directory_contents(directory_path: AnyStr, pattern: str = ".*") -> None:
    logger.debugln(" directory_path: {} pattern: {}".format(directory_path, pattern))
    regex = re.compile(pattern)
    if os.path.isdir(directory_path):
        logger.debugln(" Existing {}".format(directory_path))
        if not dry_run:
            for root, dirs, files in os.walk(directory_path):
                for f in files:
                    if regex.match(f):
                        os.unlink(os.path.join(root, f))
                for d in dirs:
                    logger.debugln(" call rmtree on root:{} d:{}".format(root, d))
                    if os.path.islink(os.path.join(root, d)):
                        os.unlink(os.path.join(root, d))
                    else:
                        shutil.rmtree(os.path.join(root, d))
    else:
        logger.debugln("rm_directory_contents NonExisting {}".format(directory_path))

# make a directory and all intermediate dirs as well
def mkdir_p(directory_path: AnyStr) -> None:
    logger.debugln(" directory_path: {} ".format(directory_path))
    if not os.path.exists(directory_path):
        if not dry_run:
            os.makedirs(directory_path)
        logger.debugln(" NonExisting {}".format(directory_path))
    else:
        logger.debugln(" Existing {}".format(directory_path))


def cp_directory():
    pass

# copy a dirrctory hierachy
def cp_directory_fulldir(src: AnyStr, dest: AnyStr) -> None:
    logger.debugln("util.cp_directory_fulldir src: {} dest: {} ".format(src, dest))
    if not dry_run:
        shutil.copytree(src, dest)
    logger.debugln("cp_directory_fulldir {} -> {}".format(src, dest))


#
# copy all the files from the src_directory_path that match the given regex patter
# to the dest_directory_path. Does NOT recurse into sub-directories
#  @param string src_directory_path
#  @param string dest_directory_path
#  @param string pattern default=".*" is a regex patter
# 
def cp_directory_files(src_directory_path: str, dest_directory_path: str, pattern=".*") -> None:
    logger.debugln(" src: {} dest: {} pattern: {} ".format(src_directory_path, dest_directory_path, pattern))
    regex = re.compile(pattern)
    if os.path.isdir(src_directory_path) and os.path.isdir(dest_directory_path):
        logger.debugln("both exist {} {} {}".format(src_directory_path, dest_directory_path, pattern))
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
    logger.debugln(" src: {} dest: {} pattern: {} ".format(src_directory_path, dest_directory_path, pattern))
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

# unpack a tar.gz file
def unpack_tar_gz(fromfile: str, todir: str) -> None:
    logger.debugln(" fromfile: {} todir: {} ".format(fromfile, todir))
    if not os.path.isdir(todir):
        raise ValueError("unpack_tar_gz toDir {} is not a dir".format(todir))
    if not os.path.isfile(fromfile):
        raise ValueError("unpack_tar_gz fromfile {} is not a file".format(todir))

    exec.run(["tar", "-xvzf", fromfile, "-C", todir])


if __name__ == '__main__':
    logger.init(logger.LOG_LEVEL_DEBUG)
    exec.run(["wget", "http://whiteacorn.com"], None)
