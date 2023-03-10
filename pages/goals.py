import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Goals',order=2)

df = px.data.gapminder()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Goals", style={'fontSize': 24, 'color': '#1a1a1a'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
                    ],width=12
                )
            ]
        )
        
    ]
)