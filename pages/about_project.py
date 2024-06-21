from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("О проекте"),
                html.Br(),
                html.P("В данном проекте производится анализ занятости населения "
                       "Российской федерации на основе датасетов с данными о занятости МСП регионов, "
                       "Занятости населения регионов, Численности населения в каждом регионе и данные о Безработице. "),
                html.Hr(style={'color': 'black'})
            ], style={'text-align': 'center'})
        )
    ]),
    ])