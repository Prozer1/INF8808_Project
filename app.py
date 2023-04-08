import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
import os

app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2 text-white"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    class_name="bg-dark",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Cristiano Ronaldo Dataviz App", style={'fontSize':50, 'textAlign':'center', 'color': '#ffffff'}))
    ]),
    
    html.Hr(),
    
    dbc.Row([
        dbc.Col([sidebar], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
        
        dbc.Col([dash.page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
    ])
], fluid=True, class_name="bg-dark vh-100")


if __name__ == "__main__":
    app.run(debug=False, port=os.getenv('PORT','8050'), host=os.getenv('HOST', '0.0.0.0'))