import os

import dash_html_components as html
import dash_core_components as dcc

from application.utils.ingestion import get_country_names
from application.model import model_load, model_train

# General data structures
try:
    data, models = model_load()
except:
    model_train()
    data, models = model_load()
    
# Country to identifier mappings
country_mapping = {'all':'All', **get_country_names()}
country_names = []

for key,country in country_mapping.items():
    if key in data.keys():
        country_names.append({'label':country,'value':key})

# Layout utils
def Header(app):
    return html.Div([get_header(app), get_menu()], className="row")


def get_header(app):
    header = html.Div(html.H1("AAVAIL"), className="six columns")
    return header


def get_menu():
    menu = html.Div(
        [
            html.Div(className="five columns"),
            html.Div(html.H4(dcc.Link(
                "Prediction",
                href="/",
            )), className="two columns"),
            html.Div(html.H4(dcc.Link(
                "Monitor",
                href="/monitor/",
            )), className="two columns")
        ],
        className="row"
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table