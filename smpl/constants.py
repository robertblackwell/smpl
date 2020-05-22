import pprint
import os
import json
from typing import Any, Dict
class Constants:
    # these constants implement the directory/file locations
    # used while installing packages

    # base name of the directory into which package repos are cloned
    clone_dir_name = "clone"

    # base name of directory into which packages are build and 'staged' before
    # final installation. This directory will mirror the structure of the finally
    # installation and will include, lib, src subdirectories
    stage_dir_name = "stage"

    # the clone and stage dirs will be located inside a "cache" the is local to each
    # project and is a direct subdirectory of the project directory.
    # the basename of this dircectory is
    cache_dir_name = ".smpl_cache"

    # basename of directory into which package include, lib, src  files are finally
    # installed. This directory will be a subdir of a project directory
    vendor_dir_name = "vendor"

