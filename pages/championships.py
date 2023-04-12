import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_4_data, question_5_data
dash.register_page(__name__, name='Championships',order=3)

df1 = question_4_data()
df2 = question_5_data()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Championships", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=px.bar(df1, x="Comp_Category", y="Goals", hover_data={"Teams": True, "Comp_Category": False, "Comp" : False,"Goals": False,}, title="Goals by Competition Category"))
                    ],width=12
                )
            ]
        )
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='bar-fig',
                            figure=px.bar(df_assist, x="Passe décisive", y="nbPasse",hover_data={"Passe décisive": False, "nbPasse": False}, title="Top 10 player to assist cristiano ronaldo"))
                
                    ], width=12
                )
            ]
        )

        
    ]
)