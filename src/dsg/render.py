from os.path import dirname, join
from pathlib import Path

import markdown
import plotly.express as px
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = join(dirname(__file__), "templates")


def bar_chart(x, y) -> str:
    fig = px.bar(x=x, y=y)
    return fig.to_html()


def render_pages():
    # read markdown files, render jinja, convert to HTML, then write to dist folder
    env = Environment(loader=FileSystemLoader(["pages", TEMPLATE_DIR]))

    # register custom jinja functions
    env.globals["bar_chart"] = bar_chart

    templ = env.get_template("index.md")
    content = markdown.markdown(templ.render())

    page_templ = env.get_template("page.html")
    page_html = page_templ.render(content=content)

    # create the dist folder if it doesn't exist
    dist_path = Path("dist")
    dist_path.mkdir(exist_ok=True)

    with open(dist_path / "index.html", "w") as outfile:
        outfile.write(page_html)
