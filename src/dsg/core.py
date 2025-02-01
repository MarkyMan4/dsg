import os
import shutil
from os.path import dirname, join
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

from dsg.connections.base import get_connection
from dsg.jinja_functions import bar_chart
from dsg.models import ProjectConfig

TEMPLATE_DIR = join(dirname(__file__), "templates")


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
    sql_path = Path(project_name, "sql")
    pages_path = Path(project_name, "pages")

    # create directories in project
    sql_path.mkdir(parents=True)
    pages_path.mkdir(parents=True)

    # load and render dsg file, then write to project directory
    env = Environment(loader=FileSystemLoader([TEMPLATE_DIR]))
    config_templ = env.get_template("dsg.yml")
    config_content = config_templ.render(project_name=project_name)

    with open(Path(project_name, "dsg.yml"), "w") as config_file:
        config_file.write(config_content)

    # copy the sample index.md file to the pages directory
    sample_index_path = Path(TEMPLATE_DIR) / "index.md"
    shutil.copy(sample_index_path, pages_path)


def load_config() -> ProjectConfig:
    config_path = Path("dsg.yml")
    if not config_path.exists():
        raise FileNotFoundError(
            "Could not find dsg.yml! Make sure you are in a dsg project directory"
        )

    with open("dsg.yml") as stream:
        config_data = yaml.safe_load(stream)

    config = ProjectConfig(**config_data)

    return config


def register_functions(env: Environment):
    env.globals["bar_chart"] = bar_chart


def render_pages(config: ProjectConfig):
    # read markdown files, render jinja, convert to HTML, then write to dist folder
    env = Environment(loader=FileSystemLoader(["pages", TEMPLATE_DIR]))
    register_functions(env)

    # load queries into environment
    conn = get_connection(config.connection)
    context = {}

    for file in os.listdir("sql"):
        filepath = Path("sql", file)
        with open(filepath) as sql_file:
            sql = sql_file.read()

        res = conn.read_sql(sql)
        key = filepath.stem
        context[key] = res

    templ = env.get_template("index.md")
    content = markdown.markdown(templ.render(**context))

    page_templ = env.get_template("page.html")
    page_html = page_templ.render(content=content)

    # create the dist folder if it doesn't exist
    dist_path = Path("dist")
    dist_path.mkdir(exist_ok=True)

    with open(dist_path / "index.html", "w") as outfile:
        outfile.write(page_html)
