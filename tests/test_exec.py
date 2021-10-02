import inspect
import os
import sys
import unittest

sys.path.append("../")

import smpl.cli_interface as cli
import smpl.config_file as cfg
import smpl.dispatcher as dispatcher
import smpl.util as util


class TestExec(unittest.TestCase):

    def test_1(self):
        util.exec_option = util.execOptionValues.stdout_only
        exec.run(["wget", "-O", "junk.wget", "http://whiteacorn.com"], None)

        # self.assertEqual(args.config_file_path, "./smpl.json")
        # self.assertEqual(cfg_obj.project_name, "project_pig")

        # self.assertEqual(y, "/home/robert/Projects/smpl/project_pig")


#
# def mainx():
#     t = test_object_test()
#     t.test_parse()


if __name__ == '__main__':
    unittest.main()
