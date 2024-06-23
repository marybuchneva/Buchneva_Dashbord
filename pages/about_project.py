from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("О проекте"),
                html.Br(),
                html.P("В датасете присутствуют данные о Занятости МСП, Занятости населения,"
                       "Численности населения и уровне Безработицы в федеральных округах и регионах Российской Федерации."
                       "В данном дашборде показана динамика показателей по всей России в целом, "
                       "по каждому федеральному округу и по каждому региону."),
                html.P("Проект на Github: https://github.com/marybuchneva/Russian_Regions_employment__statictics_Buchneva_Dashbord"),
                html.Hr(style={'color': 'black'})
            ], style={'text-align': 'center'})
        )
    ]),
    ])
