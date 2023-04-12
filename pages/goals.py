import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_8_data, question_9_data

dash.register_page(__name__, name='Goals',order=6)

df_8 = question_8_data()
# df_9 = question_9_data()

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
                            figure=px.line(df_8, x=df_8.index, y='Date', title="Goals Per Minute",
                                           labels={ "Date": "Goals" },
                                           template="plotly_dark"
                                           ))
                    ],width=12
                )
            ]
        ),
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 dcc.Graph(id='line-fig',
        #                     figure=px.line(df_9, x="Date", y="Count", color='Type', title='Type of goals per year',
        #                                     template="plotly_dark"
        #                                     ))
        #             ],width=12
        #         )
        #     ]
        # )
    ]
)