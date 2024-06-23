import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from data import df_Employment_MSP
from dash import html, dcc, callback, Output, Input
import plotly.express as px
from data import df_Employment_MSP_districts, df_Employment_MSP,df_Employment,df_Employment_district,df_Unemployment,df_Unemployment_district, counties, df_Population, df_Population_district,Population_types,age_types,all_districts, all_central_regions, all_central_regions_unique

layout = dbc.Container([
    html.Div([
        html.H3("Регион"),
        html.P(
            "Анализ основных показателей уровня занятости в конкретном регионе."
            " Используйте фильтры, чтобы увидеть результат."
            )
        ],
        style={'textAlign': 'center'}
        ),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.P("Выберите округ:")
        ], width=2),
        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-dist2',
                options=[{'label': i, 'value': i} for i in all_districts],
                value=all_districts[0],
                multi=False
            )
        ], width=8),
        ]),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.P("Выберите регион:")
            ], width=2),
            dbc.Col([
                dcc.Dropdown(
                    id='crossfilter-reg2',
                    options=[{'label': i, 'value': i} for i in all_central_regions_unique],
                    value=all_central_regions_unique[0],
                    multi=False
                )
            ], width=8),
            ]),

    html.Br(),

    html.Div(
        dcc.Graph(id='line4'),
        style={'width': '100%', 'integer': 'left', 'display': 'inline-block'}
    ),
    html.Div(
        dcc.Graph(id='bar2'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
    html.Div(
        dcc.Graph(id='line2'),
        style={'width': '50%', 'integer': 'right', 'display': 'inline-block'}
    ),

    html.Div(
            dcc.Graph(id='line5'),
            style={'width': '50%', 'integer': 'right', 'display': 'inline-block'}
        ),
    html.Div(
        dcc.Graph(id='choropleth2'),
        style={'width': '100%', 'display': 'inline-block'}
    ),
  ])

@callback(
    Output('line2', 'figure'),
    [Input('crossfilter-dist2', 'value'),
     Input('crossfilter-reg2','value')]
)
def update_line2(dist,reg):
    filtered_data = df_Employment_MSP[(df_Employment_MSP['Округ'] == dist)&(df_Employment_MSP['Субъект']==reg)].sort_values(by='Год',ascending=True)
    figure = px.line(
        filtered_data,
        x="Год",
        y='Занятость МСП',
        title="Динамика занятости МСП",
        markers=True,
    )
    figure.update_xaxes(type='category')
    return figure

@callback(
    Output('bar2', 'figure'),
    [Input('crossfilter-dist2', 'value'),
     Input('crossfilter-reg2','value')]
)
def update_bar2(dist,reg):
    filtered_data = df_Population[(df_Population['Округ'] == dist)&(df_Population['Субъект']==reg)].sort_values(by='Год',ascending=True)
    figure = px.bar(
        filtered_data,
        x='Год',
        y='Численность населения',
        color='Вид'
    )
    # figure.update_xaxes(type='category')
    return figure

@callback(
    Output('line4', 'figure'),
    [Input('crossfilter-dist2', 'value'),
     Input('crossfilter-reg2','value')]
)
def update_line4(dist,reg):
    filtered_data = df_Employment[(df_Employment['Округ'] == dist)&(df_Employment['Субъект']==reg)].sort_values(by='Год',ascending=True)
    figure = px.line(
        filtered_data,
        x="Год",
        y='Уровень занятости',
        title="Динамика уровня Занятости населения",
        markers=True,
        color='Возраст',
    )
    figure.update_xaxes(type='category')
    return figure

@callback(
    Output('line5', 'figure'),
    [Input('crossfilter-dist2', 'value'),
     Input('crossfilter-reg2','value')]
)
def update_line2(dist,reg):
    filtered_data = df_Unemployment[(df_Unemployment['Округ'] == dist) & (df_Unemployment['Субъект']==reg)].sort_values(by='Год',ascending=True)
    figure = px.line(
        filtered_data,
        x="Год",
        y='Уровень безработицы',
        title="Динамика уровня Безработицы",
        markers=True,
    )
    figure.update_xaxes(type='category')
    return figure

@callback(
     [Output('crossfilter-reg2', 'options'),
      Output('crossfilter-reg2', 'value'),],
     Input('crossfilter-dist2', 'value')
)
def update_filtres(dist):
    all_district_regions=df_Employment_MSP[df_Employment_MSP['Округ'] == dist]
    all_district_regions_unique= all_district_regions['Субъект'].unique()
    options = [{'label': i, 'value': i} for i in all_district_regions_unique]
    return options, all_district_regions_unique[0]


@callback(
    Output('choropleth2', 'figure'),
    [Input('crossfilter-dist2','value'),
    Input('crossfilter-reg2','value')]
)
def update_choropleth(dist, reg):
    filtred_data = df_Population[(df_Population['Округ'] == dist) & (df_Population['Субъект'] == reg) & (df_Population['Год'] == 2020) & (df_Population['Вид'] == 'все население')]
    figure = px.choropleth_mapbox(
        filtred_data,
        locations='cartodb_id',
        geojson=counties,
        featureidkey='properties.cartodb_id',
        # locationmode='geojson-id',
        color='Субъект',
        mapbox_style="carto-positron",
        zoom=20,
        center = {'lat':55.755773, 'lon':37.617761},
        opacity=0.5,
        hover_name='Субъект',
        hover_data={'Округ': True,'Субъект': True, 'cartodb_id': False, 'Год': False, 'Численность населения': False,},
        labels={'Округ': 'Округ','Субъект':'Регион'},
        color_continuous_scale=px.colors.sequential.Teal
    )
    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                         showlegend=False,
                         # coloraxis_showscale=False,
                         mapbox_style="carto-positron",
                         mapbox_zoom=1,
                         mapbox_center={"lat": 66, "lon": 94}
                         )
    figure.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

    return figure
