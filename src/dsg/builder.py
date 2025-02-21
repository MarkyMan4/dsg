import os
from dataclasses import dataclass
from pathlib import Path

import markdown
import markdown.blockparser
import polars as pl
import yaml
from jinja2 import Environment, FileSystemLoader

from dsg.connections.base import get_connection
from dsg.constants import (CONFIG_FILE, DIST_DIR, INDEX_FILE,
                           PAGE_TEMPLATE_FILE, PAGES_DIR, SQL_DIR,
                           TEMPLATE_DIR)
from dsg.jinja_functions import register_functions
from dsg.models import ConnectionInfo, ProjectConfig


@dataclass
class Page:
    file_stem: str  # file name without extension
    title: str
    link: str
    content: str


class SiteBuilder:
    def __init__(self):
        self.config = self._load_config()
        self.env = self._create_environment()

    def _load_config(self):
        # load config file and set up the jinja environment
        with open(CONFIG_FILE) as stream:
            config_data = yaml.safe_load(stream)

        return ProjectConfig(**config_data)

    def _create_environment(self):
        env = Environment(loader=FileSystemLoader([".", TEMPLATE_DIR]))
        register_functions(env)

        return env

    def build(self):
        """
        read markdown files, render jinja, convert to HTML, then write to dist folder
        """

        # Load queries in DataFrames and parse pages/convert to HTML. Pages are 
        # converted right away because I need to read them to get the metadata from them 
        # (e.g. page title). This metadata is needed later when writing the final HTML file
        context = self._read_queries(self.config.connection)
        pages = self._read_pages(context)
        page_links = {page.title: page.link for page in pages}

        index_page = self._parse_page(Path(INDEX_FILE), context, is_index=True)

        # create the index file first
        self._render_page(page=index_page, target_path=Path(""), links=page_links)

        # render other pages
        for page in pages:
            self._render_page(page=page, target_path=Path(PAGES_DIR), links=page_links)

    def _read_pages(self, context: dict[str, pl.DataFrame]) -> list[Page]:
        """
        Parse each page in the pages directory into a Page object
        """
        pages = []
        pages_path = Path(PAGES_DIR)

        for page in pages_path.iterdir():
            if not page.is_file():
                continue

            parsed = self._parse_page(page, context)
            pages.append(parsed)

        return pages

    def _parse_page(
        self, page: Path, context: dict[str, pl.DataFrame], is_index=False
    ) -> Page:
        """
        Given a page, render the markdown template, convert to HTML and create Page 
        object with title, link and content
        """
        md = markdown.Markdown(extensions=["meta"])
        md_templ = self.env.get_template(str(page))
        html = md.convert(md_templ.render(**context))

        # read the metadata to get the page title
        file_stem = page.stem
        metadata_title = md.Meta.get("title")
        title = (
            file_stem if metadata_title is None else metadata_title[0]
        )  # metadata is given as list, take the first element if not None

        link = f"/{file_stem}.html"
        if not is_index:
            link = f"/{PAGES_DIR}" + link

        return Page(file_stem=file_stem, title=title, link=link, content=html)

    def _render_page(self, page: Page, target_path: Path, links: dict[str, str]):
        """
        Fill in the page.html template with page content and write to dist folder
        """
        html_templ = self.env.get_template(PAGE_TEMPLATE_FILE)
        page_html = html_templ.render(
            title=page.title, content=page.content, pages=links
        )

        output_path = Path(DIST_DIR, target_path)
        output_path.mkdir(exist_ok=True)

        with open(output_path / f"{page.file_stem}.html", "w") as outfile:
            outfile.write(page_html)

    def _read_queries(self, conn_info: ConnectionInfo) -> dict[str, pl.DataFrame]:
        """
        Read queries from sql directory into dictionary where key is file name (without extension)
        and value is a polars dataframe with the query result
        """
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
