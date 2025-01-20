import argparse
import os
from pathlib import Path

import markdown

# initial contents of index.md
index_md_init = """# My DSG Project

Hello data!
"""


def initialize_project(project_name: str):
    """
    Create a new dsg project. This includes:
        - folder to put the project in
        - dsg.yml file for project configs
        - queries directory
        - pages directory with an index.md

    :param project_name: name of the project
    :type project_name: str
    """
    # TODO handle project already exists
    queries_path = Path(project_name, "queries")
    pages_path = Path(project_name, "pages")

    queries_path.mkdir(parents=True)
    pages_path.mkdir(parents=True)

    with open(Path(project_name, "dsg.yml"), "w") as config_file:
        config_file.write(f"name: {project_name}\n")

    with open(pages_path / "index.md", "w") as index_file:
        index_file.write(index_md_init)


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    init_parser = subparsers.add_parser("init", help="initialize a new project")
    subparsers.add_parser("build", help="build project as a static site")
    init_parser.add_argument("project_name")

    args = parser.parse_args()

    return args
    

def main() -> None:
    args = parse_arguments()
    
    if args.subcommand == "init":
        initialize_project(args.project_name)

    elif args.subcommand == "build":
        # to build:
        #   1. render Jinja markdown templates
        #   2. convert markdown to HTML
        with open("tests/sample_proj/index.md") as infile:
            text = infile.read()

        html = markdown.markdown(text)

        with open("index.html", "w") as outfile:
            outfile.write(html)
