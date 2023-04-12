import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from get_data import visualisation_2_data

dash.register_page(__name__, name='Opponents',order=4)

team_stats = visualisation_2_data()

# Define the data
teams = team_stats['Adversaire']
goals = team_stats['Buts']
assists = team_stats['PD']
matches = team_stats['Matches']

# Create the figure and the bar chart
fig = go.Figure(data=[
    go.Bar(name='Goals', x=teams, y=goals),
    go.Bar(name='Assists', x=teams, y=assists),
    go.Bar(name='Matches', x=teams, y=matches)
])

# Set the layout of the chart
fig.update_layout(
    title='Cristiano Ronaldo Goals, Assists, and Matches Against different teams in his Football Career',
    xaxis_title='Opponent Teams',
    yaxis_title='Number',
    barmode='group',
    template='plotly_dark'
)

# Define the layout of the app
layout = html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Opponents", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=fig)
                    ],width=12
                )
            ]
        )
])
