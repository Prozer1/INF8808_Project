import dash
from dash import dcc,html, Input, Output, State, callback, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_7_ranking_data, question_7_trophies_data

dash.register_page(__name__, name='Clubs Ranking/Trophies',order=5)

ranking_df = question_7_ranking_data()
trophies_df = question_7_trophies_data()


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
                            figure=px.line(ranking_df, x=ranking_df.index, y=ranking_df.columns, markers=True, template="plotly_dark")
                        )
                    ],width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Club Ranking", id="ranking-btn", className="me-md-2", active=True),
                        dbc.Button("Club Trophies", id="trophies-btn", active=False),
                    ],width=12, className="d-grid gap-2 d-md-flex justify-content-md-center mt-2 "
                )
            ]
        )
        
    ]
)

@callback(
    Output("line-fig", "figure"),
    Input("ranking-btn", "n_clicks"),
    Input("trophies-btn", "n_clicks"),
    prevent_initial_call=True,
)
def switch_figure(_, __):
    button_clicked = ctx.triggered_id
    if button_clicked == 'ranking-btn':
        return px.line(ranking_df, x=ranking_df.index, y=ranking_df.columns, markers=True, template="plotly_dark")
    elif button_clicked == 'trophies-btn':
        return px.bar(trophies_df, x=trophies_df.index, y=trophies_df.columns, template="plotly_dark")
