import inspect
import os
import sys
import unittest
import importlib
a1 = sys.path
y = os.path.abspath("../")
sys.path.append(os.path.abspath("../"))
a2 = sys.path
sys.path.append(os.path.abspath("../smpl"))
a3 = sys.path
# print(sys.path)


import cli_interface as cli
import config_file as cfg
import dispatcher as dispatcher
import log_module as logger 
import exec

class TestLogger(unittest.TestCase):
    def test_logger(self):
        logger.debugln("this is a test of debugln")

        # self.assertEqual(args.config_file_path, "./smpl.json")
        # self.assertEqual(cfg_obj.project_name, "project_pig")

        # self.assertEqual(y, "/home/robert/Projects/smpl/project_pig")
    def test_exec_1(self):
        exec.configure()
        exec.run(["ls"])

    def test_exec_2(self):
        exec.configure(arg_dry_run = True)
        exec.run(["ls"])

    def test_exec_3(self):
        exec.configure(arg_reporting_option = exec.REPORTING_OPT_STDOUT_ONLY)
        exec.run(["ls"])

    def test_exec_4(self):
        exec.configure(arg_reporting_option = exec.REPORTING_OPT_STDOUT_ONLY)
        exec.run(["lsx"])

    def test_exec_5(self):
        exec.configure(arg_reporting_option = exec.REPORTING_OPT_STDERR_ONLY)
        exec.run(["lsx"])

    def test_exec_6(self):
        exec.configure(arg_reporting_option = exec.REPORTING_OPT_STDERR_ONLY)
        exec.run(["ls"])

    def test_exec_7(self):
        exec.configure(arg_reporting_option = exec.REPORTING_OPT_STDERR_STDOUT_PROGRESS)
        exec.run(["tree", "/home/robert"])


#
# def mainx():
#     t = test_object_test()
#     t.test_parse()


if __name__ == '__main__':
    logger.init(logger.LOG_LEVEL_DEBUG)
    logger.set_stdout_logfile()
    unittest.main()
