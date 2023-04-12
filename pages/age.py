import dash
from dash import dcc, html, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import visualisation_1_data

dash.register_page(__name__, name='Age', order=2)

data = visualisation_1_data()

layout = dbc.Row(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Age", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Col(
            dcc.Graph(
                id='goals-graph',
                figure=px.bar(data, x='Age', y='Goals per game', title='Cristiano Ronaldo Goals per Game Ratio by Age')
            ),
            className="col-12"
        ),
        dbc.Col(
            dcc.RadioItems(
                id='mode-radio',
                options=[
                    {'label': 'Goals per game', 'value': 'Goals per game'},
                    {'label': 'Total goals', 'value': 'Total goals'},
                ],
                value='Goals per game',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                inputStyle={'margin-right': '5px'}
            ),
            className="d-flex col-12 justify-content-center m-3 fs-4 text-white",
        )
    ]
)

@callback(
    dash.dependencies.Output('goals-graph', 'figure'),
    [dash.dependencies.Input('mode-radio', 'value')]
)
def update_goals_graph(mode):
    if mode == 'Goals per game':
        return px.bar(data, x='Age', y='Goals per game', title='Cristiano Ronaldo Goals per Game Ratio by Age', template='plotly_dark')
    else:
        return px.bar(data, x='Age', y='Total goals', title='Cristiano Ronaldo Total Goals by Age', template='plotly_dark')
