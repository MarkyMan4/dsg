import plotly.express as px
import polars as pl
from jinja2 import Environment


def bar_chart(
    data: pl.DataFrame, x: str, y: str, color: str = None, title: str = None
) -> str:
    fig = px.bar(data, x=x, y=y, color=color, title=title)
    return fig.to_html()


def line_chart(
    data: pl.DataFrame, x: str, y: str, color: str = None, title: str = None
) -> str:
    fig = px.line(data, x=x, y=y, color=color, title=title)
    return fig.to_html()


def register_functions(env: Environment):
    # register the functions in this file as functions in the given environment
    env.globals[bar_chart.__name__] = bar_chart
    env.globals[line_chart.__name__] = line_chart
