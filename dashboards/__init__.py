import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from dashboards.pages import (
    monitor,
    prediction
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def create_dash_app(server):
    app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/',
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True
    )

    # Describe the layout/ UI of the app
    app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content")],
        className="container"
    )

    # Update page
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/monitor/" or pathname == "/monitor":
            return monitor.create_layout(app)
        else:
            return prediction.create_layout(app)

    @app.callback(
    dash.dependencies.Output('pred-country-message', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
    def update_output(value):
        return 'You have selected "{}"'.format(value)

    return app