import argparse
import shutil

from .core import initialize_project, load_config, render_pages


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    init_parser = subparsers.add_parser("init", help="initialize a new project")
    subparsers.add_parser("build", help="build project as a static site")
    init_parser.add_argument("project_name")
    subparsers.add_parser("clean", help="remove build artifacts")

    args = parser.parse_args()

    return args


def main() -> None:
    args = parse_arguments()

    if args.subcommand == "init":
        print(f"Initializing project {args.project_name}...")
        initialize_project(args.project_name)
        print("Your project has been initialized! Next steps:")
        print(f"cd {args.project_name}")
        print("dsg build")

    elif args.subcommand == "build":
        print(f"building...")
        config = load_config()
        render_pages(config)
        print("Build complete! The build is available in the dist folder")

    elif args.subcommand == "clean":
        try:
            print("removing dist")
            shutil.rmtree("dist")
        except:
            pass
