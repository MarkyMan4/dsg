from typing import Any

import plotly.express as px
import polars as pl
from jinja2 import Environment

# TODO allow users to define their own custom functions in dsg.yml
#      when parsing config, import from their file and load those functions to the environment
#      the only requirement for custom functions is that it returns a string to render on the page


def bar_chart(
    data: pl.DataFrame = None,
    x: Any = None,
    y: Any = None,
    color: str = None,
    title: str = None,
) -> str:
    fig = px.bar(data_frame=data, x=x, y=y, color=color, title=title)
    return fig.to_html(full_html=False)


def line_chart(
    data: pl.DataFrame = None,
    x: Any = None,
    y: Any = None,
    color: str = None,
    title: str = None,
) -> str:
    fig = px.line(data_frame=data, x=x, y=y, color=color, title=title)
    return fig.to_html(full_html=False)


def scatter_chart(
    data: pl.DataFrame = None,
    x: Any = None,
    y: Any = None,
    color: str = None,
    title: str = None,
) -> str:
    fig = px.scatter(data_frame=data, x=x, y=y, color=color, title=title)
    return fig.to_html(full_html=False)


def register_functions(env: Environment):
    # register the functions in this file as functions in the given environment
    env.globals[bar_chart.__name__] = bar_chart
    env.globals[line_chart.__name__] = line_chart
    env.globals[scatter_chart.__name__] = scatter_chart
