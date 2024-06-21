from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df_Employment_MSP_districts, df_Employment_MSP,df_Employment,df_Employment_district,df_Unemployment,df_Unemployment_district, counties, df_Population, df_Population_district,Population_types,age_types

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Россия"),
                html.P("Анализ основных показателей уровня занятости."),
                html.P("Используйте фильтр, чтобы увидеть результат."),
                html.Hr(style={'color': 'black'})
            ], style={'text-align': 'center'})
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите показатель:"),
            dbc.RadioItems(
                options=[
                    {'label': 'Численность населения', 'value': 'Численность населения'},
                    {'label': 'Занятость населения', 'value': 'Уровень занятости'},
                    {'label': 'Занятость МСП', 'value': 'Занятость МСП'},
                    {'label': 'Уровень безработицы', 'value': 'Уровень безработицы'},
                ],
                value='Занятость МСП',
                id='crossfilter-ind'
            )
        ]),
    html.Br(),
    dbc.Row([
            dbc.Col([
                html.P("Выберите вид населения (при показателе Численность)")
            ], width=10),
                dbc.Col([
                dcc.Dropdown(
                    id='crossfilter-pop',
                    options=[{'label': i, 'value': i} for i in Population_types],
                    value=Population_types[0],
                    # возможность множественного выбора
                    multi=False
                )
              ], width=8),
            ], id='crossfilter-pop-row', style= {'display': 'block'},),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.P("Выберите возраст (при показателе Занятость населения)")
            ], width=10),
            dbc.Col([
                dcc.Dropdown(
                    id='crossfilter-age',
                    options=[{'label': i, 'value': i} for i in age_types],
                    value=age_types[0],
                    multi=False
                )
                ], width=8),
            ],id='crossfilter-age-row',style= {'display': 'block'}),

        html.Br(),

        html.Div(
            dcc.Graph(id='line'),
            style={'width': '100%', 'integer': 'right', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Graph(id='choropleth'),
            style={'width': '100%', 'display': 'inline-block'}
        ),
    html.Div(id='slider-container', children=[
            dcc.Slider(
                id='crossfilter-year',
                min=df_Employment_MSP['Год'].min(),
                max=df_Employment_MSP['Год'].max(),
                value=df_Employment_MSP['Год'].min(),
                step=None,
                marks={str(year):
                           str(year) for year in df_Employment_MSP['Год'].unique()},
            )],
            style={'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),

    dbc.Col([
     dbc.Row([
        html.H5("ТОП-5 округов", style={'textAlign':'center'}),
        html.Div(id="tabletop"),
            ])

    ]),
])
    ])

@callback(
    Output('line', 'figure'),
    [Input('crossfilter-ind', 'value'),
     Input('crossfilter-pop','value'),
     Input('crossfilter-age','value')]
)
def update_line(indication,popul_type,age_type):
    if indication =='Занятость МСП':
        current_df = df_Employment_MSP_districts
        y_label ='Занятость МСП'
        filtered_data = current_df[(current_df['Округ'] == 'Российская Федерация')].sort_values(by='Год',
                                                                                                ascending=True)
    elif indication == 'Уровень занятости':
        current_df=df_Employment_district
        y_label='Уровень занятости'
        filtered_data = current_df[(current_df['Округ'] == 'Российская Федерация') & (current_df['Возраст'] == age_type)].sort_values(by='Год',ascending=True)

    elif indication =='Уровень безработицы':
        current_df = df_Unemployment_district
        y_label = 'Уровень безработицы'
        filtered_data = current_df[(current_df['Округ'] == 'Российская Федерация')].sort_values(by='Год',
                                                                                                ascending=True)

    elif indication == 'Численность населения':
        current_df = df_Population_district
        y_label = 'Численность населения'
        filtered_data = current_df[(current_df['Округ'] == 'Российская Федерация')&(current_df['Вид']==popul_type)].sort_values(by='Год',
                                                                                                                                ascending=True)
    figure = px.line(
        filtered_data,
        x="Год",
        y=y_label,
        title="Динамика в России",
        markers=True,
    )
    figure.update_xaxes(type='category')
    return figure

@callback(
    [Output('choropleth', 'figure'),
    Output('crossfilter-year', 'min'),
    Output('crossfilter-year', 'max'),
    Output('crossfilter-year', 'value'),
    Output('crossfilter-year', 'marks')],
    [Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value'),
    Input('crossfilter-pop','value'),
    Input('crossfilter-age','value')]
)
def update_choropleth(indication,year,popul_type, age_type):

    if indication =='Занятость МСП':
        current_df = df_Employment_MSP
        label = 'Занятость МСП'
    elif indication == 'Уровень занятости':
        current_df=df_Employment
        label = 'Уровень занятости'
        current_df = current_df[(current_df['Возраст'] == age_type)]
    elif indication =='Уровень безработицы':
        current_df = df_Unemployment
        label = 'Уровень безработицы'
    elif indication == 'Численность населения':
        current_df = df_Population
        label = 'Численность населения'
        current_df = current_df[(current_df['Вид'] == popul_type)]

    marks = {str(year): str(year) for year in current_df['Год'].unique()}
    if year not in current_df['Год'].unique():
        year = current_df['Год'].min()
    filtred_data = current_df[(current_df['Год'] == year)]

    figure = px.choropleth_mapbox(
        filtred_data,
        locations='cartodb_id',
        geojson=counties,
        featureidkey='properties.cartodb_id',
        # locationmode='geojson-id',
        color=indication,
        mapbox_style="carto-positron",
        zoom=20,
        center = {'lat':55.755773, 'lon':37.617761},
        opacity=0.5,
        hover_name='Субъект',
        hover_data={'Округ': True,'Субъект': False, 'cartodb_id': False, 'Год': True, indication: True,},
        labels={'Округ': 'Округ', 'Год': 'Год', indication: label,},
        color_continuous_scale=px.colors.sequential.Teal
    )
    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                         # showlegend=False,
                         # coloraxis_showscale=False,
                         mapbox_style="carto-positron",
                         mapbox_zoom=1,
                         mapbox_center={"lat": 66, "lon": 94}
                         )
    figure.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")

    return figure, current_df['Год'].min(), current_df['Год'].max(), year, marks



@callback(
    Output('crossfilter-pop-row', 'style'),
    Input('crossfilter-ind', 'value')
)
def update_dropdown_population_visibility(indication):
    if indication =='Численность населения':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@callback(
    Output('crossfilter-age-row', 'style'),
    Input('crossfilter-ind', 'value')
)
def update_dropdown_employment_visibility(indication):
    if indication == 'Уровень занятости':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@callback(
    Output('tabletop', 'children'),
    [Input('crossfilter-ind', 'value'),
    Input('crossfilter-year', 'value'),
    Input('crossfilter-pop','value'),
    Input('crossfilter-age','value')]
)
def update_table(indication, year, popul_type,age_type):
    if indication == 'Занятость МСП':
        current_df = df_Employment_MSP_districts
        filtred_data = current_df[(current_df['Год'] == year) & (current_df['Округ'] != 'Российская Федерация') &
                                  (current_df['Округ'])].sort_values(by=indication, ascending=False)
    elif indication == 'Уровень занятости':
        current_df = df_Employment_district
        filtred_data = current_df[(current_df['Год'] == year) & (current_df['Округ'] != 'Российская Федерация') & (current_df['Возраст']==age_type) & (current_df['Округ'])].sort_values(by=indication, ascending=False)
    elif indication == 'Уровень безработицы':
        current_df = df_Unemployment_district
        filtred_data = current_df[(current_df['Год'] == year) & (current_df['Округ'] != 'Российская Федерация') &
                                  (current_df['Округ'])].sort_values(by=indication, ascending=False)
    elif indication == 'Численность населения':
        current_df = df_Population_district
        filtred_data = current_df[(current_df['Год'] == year) & (current_df['Округ'] != 'Российская Федерация') & (current_df['Вид']==popul_type) &
                                  (current_df['Округ'])].sort_values(by=indication, ascending=False)
    # filtred_data = current_df[(current_df['Год'] == year) & (current_df['Округ']!='Российская Федерация') &
    #     (current_df['Округ'])].sort_values(by=indication, ascending=False)
    data_table = filtred_data.iloc[0:5][['Округ', indication]]
    table = dbc.Table.from_dataframe(
        data_table, striped=True, bordered=True, hover=True, index=False)
    return table