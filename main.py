import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages import country, district, region, about_project


external_stylesheets = [dbc.themes.PULSE]
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#c8a2c8", # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Статистика округов и регионов России", className="display-6"),
        html.Hr(),
        html.P(
            "Учебный проект студентов БСБО-14-21", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("О проекте", href="/", active="exact"),
                dbc.NavLink("Страна", href="/page-1", active="exact"),
                dbc.NavLink("Округ", href="/page-2", active="exact"),
                dbc.NavLink("Регион", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return about_project.layout
    if pathname == "/page-1":
        return country.layout
    elif pathname == "/page-2":
        return district.layout
    elif pathname == "/page-3":
        return region.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__=='__main__':
    app.run_server(debug= True, port=8051)
