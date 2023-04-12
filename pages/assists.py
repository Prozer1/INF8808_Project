import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_10_data
dash.register_page(__name__, name='Assists',order=7)

df = question_10_data()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Assists", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=px.bar(df, x="Passe décisive", y="nbPasse",hover_data={"Passe décisive": False, "nbPasse": False}, title="Top 10 player to assist cristiano ronaldo"))
                    ],width=12
                )
            ]
        )
        
    ]
)