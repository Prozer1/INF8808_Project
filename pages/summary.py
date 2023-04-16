import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Accueil', path='/',order=1)

df = px.data.gapminder()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Accueil", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("L'équipe 3 - SportsAI", style={'fontSize': 18, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
                 dbc.Col(
                    [
                        html.Div("Samia Safaa, Sanmar Simon, Ayman Atmani", style={'fontSize': 18, 'color': '#ffffff'}),
                        html.Div("Hugo Juillet, Abderrahmane Grou", style={'fontSize': 18, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        
    ]
)