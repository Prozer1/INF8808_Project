import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Accueil', path='/',order=1)

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Samia"), html.Td("Safaa")])
row2 = html.Tr([html.Td("Abderrahmane"), html.Td("Grou")])
row3 = html.Tr([html.Td("Ayman"), html.Td("Atmani")])
row4 = html.Tr([html.Td("Sanmar"), html.Td("Simon")])
row5 = html.Tr([html.Td("Hugo"), html.Td("Juillet")])

table_body = [html.Tbody([row1, row2, row3, row4, row5])]

table = dbc.Table(
    # using the same table as in the above example
    table_header + table_body,
    bordered=True,
    dark=True,
    hover=True,
    responsive=True,
    striped=True,
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Accueil", style={'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("L'équipe 3 - SportsAI", style={'fontSize': 20, 'color': '#ffffff'}),
                        table
                    ], className='p-3',xs=10, sm=10, md=8, lg=6, xl=6, xxl=6
                ),
                dbc.Col(
                    [
                        html.Img(src='./assets/cristiano_pic.png', height='500')
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Dans le cadre de notre projet visant à analyser l'impact de Ronaldo sur le sport, nous utilisons la visualisation de données pour explorer certains des moments clés et des réalisations de sa carrière. En représentant graphiquement les données relatives aux buts, aux passes décisives et à d'autres statistiques de Ronaldo, nous sommes en mesure de mieux comprendre son style de jeu, ses forces et ses faiblesses, ainsi que l'impact qu'il a eu sur ses équipes et sur le sport dans son ensemble.", style={'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=6, xl=6, xxl=6
                )
            ]
        )
        
    ]
)