import inspect
import os
import sys
import unittest

sys.path.append("../")

import smpl.cli_interface as cli
import smpl.config_file as cfg
import smpl.dispatcher as dispatcher


class TestCli(unittest.TestCase):

    def test_1(self):
        os.chdir("../project_pig")
        y = os.getcwd()
        p = cli.define_cli_interface()
        args = p.parse_args(["--config-file", "./smpl.json"])
        cfg_obj = cfg.ConfigObject(args)

        self.assertEqual(args.config_file_path, "./smpl.json")
        self.assertEqual(cfg_obj.project_name, "project_pig")

        self.assertEqual(y, "/home/robert/Projects/smpl/project_pig")

    def test_2(self):
        os.chdir("../project_pig")
        y = os.getcwd()
        p = cli.define_cli_interface()
        args = p.parse_args(["--config-file", "./smpl.json", "install", "boost"])
        subcmd = args.subcmd
        subcmd_arg = args.subcmd_arg
        cfg_obj = cfg.ConfigObject(args)
        dispatcher.dispatch(subcmd, subcmd_arg, cfg_obj)
        self.assertEqual(args.config_file_path, "./smpl.json")
        self.assertEqual(cfg_obj.project_name, "project_pig")

        self.assertEqual(y, "/home/robert/Projects/smpl/project_pig")

#
# def mainx():
#     t = test_object_test()
#     t.test_parse()


if __name__ == '__main__':
    unittest.main()
