import plotly.express as px
import polars as pl


def bar_chart(data: pl.DataFrame, x: str, y: str) -> str:
    fig = px.bar(data, x=x, y=y)
    return fig.to_html()
