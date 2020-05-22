import argparse

#
# define global argument and options
#
def define_global_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--version, -v', dest='version',
                        help='Print version ')
    parser.add_argument('--config-file', dest='config_file_path',
                        help='Path of a json/yaml config file, alternative to command '
                             ' line options.\n Default smpl.json')

    parser.add_argument('--project-name', dest='project_name',
                        help='The name of the project. Required')

    parser.add_argument('--project-dir', dest='project_dir',
                        help='Path to the project top level directory. Defaults to basename of pwd/cwd and MUST be '
                             'same as basename '
                             'of cwd. ')

    # parser.add_argument('--clean-before', dest='clean_before_flag', action='store_true',
    #                     help='Clean vendor, stage clone directories before starting install ')

    parser.add_argument('--log-actions', dest='log_actions', action='store_true',
                        help='Creates a log of all cli commands and their output.')

    parser.add_argument('--action-logfile', dest='log_path',
                        help='path of file for logging actions. Default ./simpli_log.log')

    # parser.add_argument('--clone-dir', dest='clone_dir_path',
    #                     help='''The path for directory into which packages are cloned/unpacked.
    #             Default to scripts/clone ''')
    #
    # parser.add_argument('--stage-dir', dest='stage_dir_path',
    #                     help='''The path for directory into which package headers amd archives
    #         are copied after building. Default to scripts/stage ''')
    #
    # parser.add_argument('--vendor-dir', dest='vendor_dir_path',
    #                     help='''The path for directory into which package headers amd archives are installed locally
    #                     for the project.\n Must always be an immediate subdirectory of the project-dir and defaults
    #                     to {project-dir}/vendor.''')
    #
    # parser.add_argument('--external-dir', dest='external_dir_path',
    #                     help='''The path for directory into which packages delivered as copied source files will be
    #                     installed.\n Must be inside the project source directory.\n Defaults to
    #                     project_dir/source_dir_name/external. TODO: provide an option to install source-only packages
    #                     into {project_dir}/vendor''')


#
# define subcommands and their arguments/options
#
def define_subcommands(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(title='Sub Commands')

    #
    # download subcommand
    #
    parser_download = subparsers.add_parser(name="download",
                                            help="downloads one dependency (name provided as arg) or all "
                                                 "dependenciesies into the repo cache using either git clone or wget")
    parser_download.add_argument('subcmd_arg', nargs="?", type=str,
                                 help='optional - a name of a dependency, if ommited means all')
    parser_download.set_defaults(subcmd="download")

    #
    # build subcommand
    #
    parser_build = subparsers.add_parser(name="build",
                                         help="builds one dependency (name provided as arg) or all dependencies and "
                                              "copies the exportable files to their appropriate directory in the "
                                              "stage directory")
    parser_build.add_argument('subcmd_arg', nargs="?", type=str,
                              help='optional - a name of a dependency, if ommited means all')
    parser_build.set_defaults(subcmd="build")

    #
    # vendor subcommand
    #
    parser_vendor = subparsers.add_parser(name="install",
                                          help="copy the exportable files of one dependency (name provided as arg)"
                                               "or all dependencies into the vendor directory")
    parser_vendor.add_argument('subcmd_arg', nargs="?", type=str,
                               help='optional - a name of a dependency, if ommited means all')
    parser_vendor.set_defaults(subcmd="install")

    #
    # install subcommand
    #
    parser_install = subparsers.add_parser(name="all",
                                           help="download, build and copy to vendor either a single "
                                                "dependency (name provided as arg) or all dependencies"
                                                " if no arg provided")
    parser_install.add_argument('subcmd_arg', nargs="?", type=str, help='optional - a name of a dependency, '
                                                                        'if ommited means all')
    # parser_install.set_defaults(parser_install=True)
    parser_install.set_defaults(subcmd="all")

    #
    # clean subcommand
    #
    parser_clean = subparsers.add_parser(name="clean",
                                         help="removes all installation artifacts for all dependencies")
    parser_clean.add_argument('subcmd_arg', nargs="?", type=str, help='optional - a name of a dependency, '
                                                                      'if ommited means all')
    parser_clean.set_defaults(subcmd="clean")
    #
    # list subcommand
    #
    parser_clean = subparsers.add_parser(name="list",
                                         help="lists the packages in the config file")
    parser_clean.add_argument('subcmd_arg', nargs="?", type=str, help='optional - a name of a dependency, '
                                                                      'if ommited means all')
    parser_clean.set_defaults(subcmd="list")


def define_cli_interface() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install dependencies for project.")
    parser.add_argument('-v', '--version', action="store_true",
                        help="Prints the version number.")
    define_global_args(parser)
    define_subcommands(parser)
    return parser
