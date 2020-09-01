import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dashboards.utils.utils import Header, make_dash_table

import pandas as pd



def create_layout(app):
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    fig = go.Figure([
        go.Scatter(x=df['Date'], y=df['AAPL.High'], fill=None, line_color='gray'),
        go.Scatter(x=df['Date'], y=df['AAPL.Low'], fill="tonexty", line_color="gray"),
        go.Scatter(x=df['Date'], y=df['AAPL.Close'])
    ])
    fig.update_layout(showlegend=False)

    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            html.Div([
                html.H3("Prediction"),
                html.Div([
                    "Select country",
                    html.Div(id="pred-country-message"),
                    dcc.Dropdown(
                        options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montreal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'},
                        ],
                        value='MTL',
                        id="demo-dropdown",
                        clearable=False
                    )
                ], className="row"),

                html.Br([]),
                html.Div([
                    dcc.Graph(figure=fig)
                ])
            ])
        ]
    )

