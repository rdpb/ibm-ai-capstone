import dash
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def create_dash_app(server):
    app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/',
        external_stylesheets=external_stylesheets
    )

    app.layout = html.Div("My Dash app")

    return app