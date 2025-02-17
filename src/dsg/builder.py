import os
from pathlib import Path

import markdown
import polars as pl
import yaml
from jinja2 import Environment, FileSystemLoader

from dsg.connections.base import get_connection
from dsg.constants import (CONFIG_FILE, DIST_DIR, INDEX_FILE,
                           PAGE_TEMPLATE_FILE, PAGES_DIR, SQL_DIR,
                           TEMPLATE_DIR)
from dsg.jinja_functions import register_functions
from dsg.models import ConnectionInfo, ProjectConfig


class SiteBuilder:
    def __init__(self):
        self.config = self._load_config()
        self.env = self._create_environment()
        self.pages = self._make_page_links()

    def _load_config(self):
        # load config file and set up the jinja environment
        with open(CONFIG_FILE) as stream:
            config_data = yaml.safe_load(stream)

        return ProjectConfig(**config_data)

    def _create_environment(self):
        env = Environment(loader=FileSystemLoader([".", TEMPLATE_DIR]))
        register_functions(env)

        return env

    def _make_page_links(self) -> dict[str, str]:
        # mapping from page name to link to be used in href
        pages_path = Path(PAGES_DIR)
        pages_links = {}

        for page in pages_path.iterdir():
            page_name = page.stem
            pages_links[page_name] = f"/{PAGES_DIR}/{page_name}.html"

        return pages_links

    def build(self):
        # read markdown files, render jinja, convert to HTML, then write to dist folder
        # TODO disallow index.md in pages directory
        context = self._read_queries(self.config.connection)

        # create the index file first
        self._render_page(
            source_file=Path(INDEX_FILE), target_path=Path("."), context=context
        )

        # render other pages
        pages_content = {}  # mapping from page name to rendered html
        pages_path = Path(PAGES_DIR)

        for page_file in pages_path.iterdir():
            if not page_file.is_file():
                continue

            self._render_page(
                source_file=page_file, target_path=pages_path, context=context
            )

    def _render_page(
        self, source_file: Path, target_path: Path, context: dict[str, pl.DataFrame]
    ):
        # render markdown template and convert to html
        md_templ = self.env.get_template(str(source_file))
        content = markdown.markdown(md_templ.render(**context))

        # render HTML page by injecting rendered markdown into page template, and write to dist folder
        # TODO allow user defined page title
        base_file_name = source_file.stem
        html_templ = self.env.get_template(PAGE_TEMPLATE_FILE)
        page_html = html_templ.render(
            title=base_file_name, content=content, pages=self.pages
        )

        output_path = Path(DIST_DIR, target_path)
        output_path.mkdir(exist_ok=True)

        with open(output_path / f"{base_file_name}.html", "w") as outfile:
            outfile.write(page_html)

    def _read_queries(self, conn_info: ConnectionInfo) -> dict[str, pl.DataFrame]:
        # read queries from sql directory into dictionary where key is file name (without extension)
        # and value is a polars dataframe with the query result
        conn = get_connection(conn_info)
        query_results = {}

        for file in os.listdir(SQL_DIR):
            filepath = Path(SQL_DIR, file)
            with open(filepath) as sql_file:
                sql = sql_file.read()

            res = conn.read_sql(sql)
            key = filepath.stem
            query_results[key] = res

        return query_results
