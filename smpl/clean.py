import os
import smpl.util as util
import smpl.config_file as cfg


def clean_install_dirs(cfg_obj: cfg.ConfigObject) -> None:
    util.clear_directory(cfg_obj.clone_dir)
    util.clear_directory(cfg_obj.stage_dir)
    util.clear_directory(os.path.join(cfg_obj.vendor_dir, "include"))
    util.clear_directory(os.path.join(cfg_obj.vendor_dir, "lib"))
    util.clear_directory(os.path.join(cfg_obj.vendor_dir, "ssl"))


def clean_only(cfg_obj: cfg.ConfigObject) -> None:
    """
    removes all directories used during installation, Would neeed to do this to clean up
    prior to changing the names and locations of some of the install locations
    """
    util.rm_directory(cfg_obj.clone_dir)
    util.rm_directory(cfg_obj.stage_dir)
    util.rm_directory(os.path.join(cfg_obj.vendor_dir))

