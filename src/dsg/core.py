import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from dsg.builder import SiteBuilder
from dsg.constants import (CONFIG_FILE, INDEX_FILE, PAGES_DIR, SQL_DIR,
                           TEMPLATE_DIR)


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
    project_path = Path(project_name)
    sql_path = project_path / SQL_DIR
    pages_path = project_path / PAGES_DIR

    # create directories in project
    sql_path.mkdir(parents=True)
    pages_path.mkdir(parents=True)

    # load and render dsg file, then write to project directory
    env = Environment(loader=FileSystemLoader([TEMPLATE_DIR]))
    config_templ = env.get_template(CONFIG_FILE)
    config_content = config_templ.render(project_name=project_name)

    with open(project_path / CONFIG_FILE, "w") as config_file:
        config_file.write(config_content)

    # copy the sample index.md file to the pages directory
    sample_index_path = Path(TEMPLATE_DIR) / INDEX_FILE
    shutil.copy(sample_index_path, project_path)


def check_required_files() -> bool:
    is_missing_files = False

    # ensure the dsg.yml and index.md files exist
    index_path = Path(INDEX_FILE)
    if not index_path.exists():
        print("Could not find index.md! This file is required as your home page")
        is_missing_files = True

    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        print("Could not find dsg.yml! Make sure you are in a dsg project directory")
        is_missing_files = True

    return is_missing_files


def build_site():
    builder = SiteBuilder()
    builder.build()
