import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dashboards.utils.utils import Header, make_dash_table

import pandas as pd

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            html.Div(
                [html.H3("Monitor")]
            )
        ]
    )