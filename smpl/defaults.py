import os

class Defaults:
    def __init__(self, the_project_name, the_project_dir):
        self.project_name = the_project_name
        self.project_dir = the_project_dir
        self.external_name = "external_src"
        self.vendor_name = "vendor"
        self.scripts_name = "scripts"
        self.clone_name = "clone"
        self.stage_name = "stage"
        self.clone_dir = os.path.join(the_project_dir, self.scripts_name, self.clone_name)
        self.stage_dir = os.path.join(the_project_dir, self.scripts_name, self.stage_name)
        self.unpack_dir = os.path.join(the_project_dir, self.scripts_name, self.clone_name)
        self.source_dir = os.path.join(the_project_dir, the_project_name)
        self.external_dir = os.path.join(the_project_dir, the_project_name, self.external_name)
        self.vendor_dir = os.path.join(the_project_dir, self.vendor_name)
        self.dependencies = {}


def validate_and_construct_names(args) -> Defaults:
    if args.project_name is None: 
        print("Error: project name is required")
        exit()
    if args.project_dir is None: 
        project_dir = os.getcwd()
    else:
        project_dir = args.project_dir

    defaults = Defaults(args.project_name, project_dir)

    a = defaults.project_name.lower()
    b = os.path.basename(defaults.project_dir).lower()
    xx = (a != b)
    if defaults.project_name.lower() != os.path.basename(defaults.project_dir).lower():
        print("project name [%s] and current working directory [%s] have conflict" % (defaults.project_name.lower(), os.path.basename(defaults.project_dir).lower()))
        exit()

    if args.source_dir_name is None:
        defaults.source_dir = os.path.join(defaults.project_dir, defaults.project_name.lower())
    else:
        defaults.source_dir = os.path.join(defaults.project_dir, args.source_dir_name)

    if not os.path.isdir(defaults.source_dir):
        print("The given source dir [%s] does not exist" % defaults.source_dir)
        exit()
    if os.path.realpath(os.path.join(defaults.source_dir, "../")) != defaults.project_dir:
        print("The given source dir [%s] is not an immediate subdir of the project dir [%s]" % (defaults.source_dir, defaults.project_dir))
        exit()

    defaults.script_dir = os.path.join(defaults.project_dir, 'scripts')
    if args.clone_dir_path:
        defaults.clone_dir = os.path.abspath(args.clone_dir_path)
    else:
        defaults.clone_dir = os.path.join(defaults.script_dir, 'clone')
    
    if args.stage_dir_path:
        defaults.stage_dir = os.path.abspath(args.stage_dir_path)
    else:
        defaults.stage_dir = os.path.join(defaults.script_dir, 'stage')
    
    if args.vendor_dir_path:
        defaults.vendor_dir = os.path.abspath(args.vendor_dir_path)
    else:
        defaults.vendor_dir = os.path.join(defaults.project_dir, 'vendor')
    
    if args.external_dir_path:
        defaults.external_dir = os.path.abspath(args.external_dir_path)
    else:
        defaults.external_dir = os.path.join(defaults.source_dir, 'external')

    for d in args.dependencies:
        defaults.dependencies[d.name] = d.parms
    return defaults

