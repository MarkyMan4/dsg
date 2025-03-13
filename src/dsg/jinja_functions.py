from typing import Any

import plotly.express as px
import polars as pl
from jinja2 import Environment

# TODO allow users to define their own custom functions in dsg.yml
#      when parsing config, import from their file and load those functions to the environment
#      the only requirement for custom functions is that it returns a string to render on the page

def table(data: pl.DataFrame = None):
    # TODO implement this
    pass

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
    size: Any = None,
    color: str = None,
    title: str = None,
) -> str:
    fig = px.scatter(data_frame=data, x=x, y=y, size=size, color=color, title=title)
    return fig.to_html(full_html=False)


def pie_chart(
    data: pl.DataFrame = None,
    values: Any = None,
    names: Any = None,
    color: str = None,
    title: str = None,
) -> str:
    fig = px.pie(data_frame=data, values=values, names=names, color=color, title=title)
    return fig.to_html(full_html=False)


def histogram_chart(
    data: pl.DataFrame = None,
    x: Any = None,
    y: Any = None,
    nbins: Any = None,
    color: str = None,
    title: str = None,
) -> str:
    fig = px.histogram(data_frame=data, x=x, y=y, nbins=nbins, color=color, title=title)
    return fig.to_html(full_html=False)


def histogram_2d_chart(
    data: pl.DataFrame = None,
    x: Any = None,
    y: Any = None,
    values: Any = None,
    nbinsx: Any = None,
    nbinsy: Any = None,
    names: Any = None,
    title: str = None,
) -> str:
    fig = px.density_heatmap(
        data_frame=data,
        x=x,
        y=y,
        values=values,
        nbinsx=nbinsx,
        nbinsy=nbinsy,
        names=names,
        title=title,
    )
    return fig.to_html(full_html=False)


def heatmap_chart(
    data: pl.DataFrame = None,
    title: str = None,
    x: Any = None,
    y: Any = None,
    text_auto: bool = True,
) -> str:
    fig = px.imshow(data_frame=data, x=x, y=y, text_auto=text_auto, title=title)
    return fig.to_html(full_html=False)


def register_functions(env: Environment):
    # register the functions in this file as functions in the given environment
    env.globals[bar_chart.__name__] = bar_chart
    env.globals[line_chart.__name__] = line_chart
    env.globals[scatter_chart.__name__] = scatter_chart
    env.globals[pie_chart.__name__] = pie_chart
    env.globals[histogram_chart.__name__] = histogram_chart
    env.globals[histogram_2d_chart.__name__] = histogram_2d_chart
    env.globals[heatmap_chart.__name__] = heatmap_chart
