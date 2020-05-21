import argparse
import pprint
import os

pp = pprint.PrettyPrinter(indent=4)

project_name = "marvin++"
project_dir = os.getcwd()
source_dir = os.path.join(project_dir, "marvin")
clone_dir = os.path.join(project_dir, "scripts", "clone_dir")
stage_dir = os.path.join(project_dir, "scripts", "stage_dir")

__version__ = "0.3.5"

debug = True
logfile = False


# a class that holds project defaults
class Defaults:
    def __init__(self, the_project_name, the_project_dir):
        self.project_name = the_project_name
        self.project_dir = the_project_dir
        self.clone_name = "clone"
        self.stage_name = "stage"
        self.external_name = "external"
        self.vendor_name = "vendor"
        self.scripts_name = "scripts"
        self.unpack_dir = os.path.join(project_dir, self.scripts_name, self.clone_name)
        self.source_dir = os.path.join(project_dir, the_project_name)
        self.external_dir = os.path.join(project_dir, the_project_name, self.external_name)
        self.vendor_dir = os.path.join(project_dir, self.vendor_name)


def doit(openssl_version, output_dir, dryrun_flag):
    print("Hello")
    pp.pprint([openssl_version, output_dir, dryrun_flag])


def main():
    project_name = None
    project_dir = None
    source_dir_name = None

    parser = argparse.ArgumentParser(
        description="Install dependencies for project.")
    parser.add_argument('-v', '--version', action="store_true",
                        help="Prints the version number.")

    parser.add_argument('--install', dest="install_flag", action="store_true",
                        help='Installs the staged install to the final destination')

    parser.add_argument('--project-name', dest='project_name', help='The name of the project. Required')
    parser.add_argument('--project-dir', dest='project_dir',
                        help='Path to the project top level directory. Defaults to pwd. ')
    parser.add_argument('--source-dir-name', dest='project_dir_name',
                        help='Stem name of the project source directory, should be same as project name lowercased')

    parser.add_argument('--clone-dir', dest='clone_dir_path',
                        help='The path for directory into which packages are cloned/unpacked. Default to '
                             'scripts/clone_dir ')
    parser.add_argument('--stage-dir', dest='stage_dir_path',
                        help='The path for directory into which package headers amd archives are copied after building.'
                             + 'Default to scripts/stage ')
    parser.add_argument('--vendor-dir', dest='vendor_dir_path',
                        help='The path for directory into which package headers amd archives are installed locally to '
                             'the project.\n '
                             + 'Mustb always be an immediate subdirectory of the project-dir and defaults to {'
                               'project-dir}/vendor.')
    # 													+ 'and libraries will be in {install-dir}/lib')
    parser.add_argument('--external-dir', dest='external_dir_path',
                        help='The path for directory into packages delivered as copied source files will be '
                             'installed.\n '
                             'Must be inside the project source directory, Defaults to '
                             'project_dir/source_dir_name/external.')

    args = parser.parse_args()
    pp.pprint(args)

    if __name__ == "__main__":
        main()