import dash
from dash import dcc,html, Input, Output, callback, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
from get_data import question_8_data, question_9_data

dash.register_page(__name__, name='Goals',order=6)

df_8 = question_8_data()
df_9 = question_9_data()

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
                        dcc.Graph(id='graph-fig',
                            figure=px.line(df_8, x=df_8.index, y='Date', title="Goals per minute",
                                           labels={ "Date": "Goals" },
                                           template="plotly_dark"
                                           ))
                    ],width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Goals Per Minute", id="minute-btn",color='info', className="me-md-2"),
                        dbc.Button("Goal Types", id="type-btn", color='primary'),
                    ],width=12, className="d-grid gap-2 d-md-flex justify-content-md-center mt-2 "
                )
            ]
        )
    ]
)

@callback(
    [Output("graph-fig", "figure"),
     Output("minute-btn", "color"),
     Output("type-btn", "color")],
    Input("minute-btn", "n_clicks"),
    Input("type-btn", "n_clicks"),
    prevent_initial_call=True,
)
def switch_figure(_, __):
    button_clicked = ctx.triggered_id
    if button_clicked == 'minute-btn':
        return (px.line(df_8, x=df_8.index, y='Date', title="Goals per minute", labels={ "Date": "Goals" }, template="plotly_dark"), 'info', 'primary')
    elif button_clicked == 'type-btn':
        return (px.line(df_9, x="Date", y="Count", color='Type', title='Type of goals per year',template="plotly_dark"), 'primary', 'info')