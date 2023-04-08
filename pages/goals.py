import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_8_data

dash.register_page(__name__, name='Goals',order=6)

df = question_8_data()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Goals", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=px.line(df, x=df.index, y='Date', title="Goals Per Minute",
                                           labels={ "Date": "Goals" },
                                           template="plotly_dark"
                                           ))
                    ],width=12
                )
            ]
        )
        
    ]
)