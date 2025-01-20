import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    init_parser = subparsers.add_parser("init", help="initialize a new project")
    build_parser = subparsers.add_parser("build", help="build project as a static site")
    init_parser.add_argument("project_name")
    build_parser.add_argument("test")

    args = parser.parse_args()

    return args
    

def main() -> None:
    args = parse_arguments()
    
    if args.subcommand == "init":
        print("initialize new project")
    elif args.subcommand == "build":
        pass
