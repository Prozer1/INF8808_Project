import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_7_data

dash.register_page(__name__, name='Clubs Ranking/Trophies',order=5)

df = question_7_data()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Clubs Ranking/Trophies", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=px.line(df, x=df.index, y=df.columns, markers=True, template="plotly_dark"))
                    ],width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Club Ranking", className="me-md-2"),
                        dbc.Button("Club Trophies"),
                    ],width=12, className="d-grid gap-2 d-md-flex justify-content-md-center mt-2 "
                )
            ]
        )
        
    ]
)