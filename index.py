import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
import sqlalchemy
from datetime import datetime


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

tabs_styles = {
    "flex-direction": "row",
}
tab_style = {
    "padding": "1.3vh",
    "color": 'black',
    "fontSize": '.9vw',
    "backgroundColor": 'rgba(242, 242, 242, 0.0)',
    'border-bottom': '1px black solid',

}

tab_selected_style = {
    "fontSize": '.9vw',
    "color": 'black',
    "padding": "1.3vh",
    'fontWeight': 'bold',
    "backgroundColor": '#b6c0c8',
    'border-top': '1px black solid',
    'border-left': '1px black solid',
    'border-right': '1px black solid',
    'border-radius': '0px 0px 0px 0px',
}

tab_selected_style1 = {
    "fontSize": '.9vw',
    "color": '#F4F4F4',
    "padding": "1.3vh",
    'fontWeight': 'bold',
    "backgroundColor": '#566573',
    'border-top': '1px white solid',
    'border-left': '1px white solid',
    'border-right': '1px white solid',
    'border-radius': '0px 0px 0px 0px',
}

chart_humidity = dcc.Graph(id = 'humidity_chart',
                           animate=True,
                           config = {'displayModeBar': 'hover'},
                           className = 'chart_width'),

chart_temperature = dcc.Graph(id = 'temperature_chart',
                              animate=True,
                              config = {'displayModeBar': 'hover'},
                              className = 'chart_width')

app.layout = html.Div([
    html.Div(id = 'background_image'),
    html.Div([
        dcc.Interval(id = 'update_date_time',
                     interval = 1000,
                     n_intervals = 0),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.H6('DHT11 Sensor Data',
                        style = {
                            'line-height': '1',
                            'color': 'white'},
                        className = 'adjust_title six columns'
                        ),
                html.Div([
                    html.Div(id = 'update',
                             className = 'image_grid six columns'),
                    html.H6(id = 'get_date_time',
                            style = {
                                'line-height': '1',
                                'color': 'white'},
                            className = 'adjust_date_time'
                            )
                ], className = 'temp_card1'),
            ], className = 'adjust_title_and_date_time_two_columns')
        ], className = 'container_title_date_time twelve columns')
    ], className = "row flex-display"),
    html.Div([
        dcc.Interval(id = 'update_chart',
                     interval = 1000,
                     n_intervals = 0),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.Div(id = 'text1', className = 'grid_height'),
                html.Div(id = 'text2', className = 'grid_height'),
            ], className = 'grid_two_column'),

            html.Div([
                dcc.Tabs(id = "tabs-styled-with-inline", value = 'chart_temperature', children = [
                    dcc.Tab(chart_humidity,
                            label = 'Humidity',
                            value = 'chart_humidity',
                            style = tab_style,
                            selected_style = tab_selected_style,
                            className = 'font_size'),
                    dcc.Tab(chart_temperature,
                            label = 'Temperature',
                            value = 'chart_temperature',
                            style = tab_style,
                            selected_style = tab_selected_style,
                            className = 'font_size'),
                ], style = tabs_styles,
                         colors = {"border": None,
                                   "primary": None,
                                   "background": None}),

            ], className = 'create_container3 twelve columns'),
        ], className = 'adjust_grids'),
    ], className = "row flex-display"),

], id= "mainContainer",
   style={"display": "flex", "flex-direction": "column"})

@app.callback(Output('background_image', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:sql_root_45t6@localhost:3306/humidity_and_temperature')
    # df = pd.read_sql_table('humiditytemperature', engine)
    # df.to_csv('data.csv')
    # df1 = pd.read_csv('data.csv')
    header_list = ['Time', 'Humidity', 'Temperature']
    df = pd.read_csv('humidity_and_temperature.csv', names = header_list)
    # get_time = df['Time'].tail(1).iloc[0].strftime("%Y-%m-%d %H:%M:%S")
    get_time = df['Time'].tail(1).iloc[0]
    get_temp = df['Temperature'].tail(1).iloc[0].astype(float)
    # previous_temp = df['Temperature'].tail(2).iloc[0].astype(float)
    # change_temperature = get_temp - previous_temp
    if n_intervals == 0:
        raise PreventUpdate

    if get_temp >= 21:

     return [
        html.Div(style = {'background-image': 'url("/assets/sunny.jpg")',
                          'height': '100vh',
                          'background-repeat': 'no-repeat',
                          'background-size': 'auto'
                          }),
     ]

    elif get_temp < 21:
        return [
            html.Div(style = {'background-image': 'url("/assets/cloudy.jpg")',
                              'height': '100vh',
                              'background-repeat': 'no-repeat',
                              'background-size': 'auto'
                              },
                     ),

        ]

@app.callback(Output('get_date_time', 'children'),
              [Input('update_date_time', 'n_intervals')])
def update_graph(n_intervals):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if n_intervals == 0:
        raise PreventUpdate

    return [
        html.Div(dt_string),
    ]

@app.callback(Output('humidity_chart', 'figure'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:sql_root_45t6@localhost:3306/humidity_and_temperature')
    # df = pd.read_sql_table('humiditytemperature', engine)
    # df.to_csv('data.csv')
    # df1 = pd.read_csv('data.csv')
    header_list = ['Time', 'Humidity', 'Temperature']
    df = pd.read_csv('humidity_and_temperature.csv', names = header_list)
    # timeArray = []
    # humiArray = []
    # print(humiArray)
    # tempArray = []
    get_time = df['Time'].tail(20)
    # X = deque(maxlen = 100)
    # timeArray.append(get_time)
    # print(get_time)
    get_humi = df['Humidity'].tail(20)
    # Y = deque(maxlen = 100)
    # humiArray.append(get_humi)
    # print(get_humi)
    # timeArray.append(get_time)
    # humiArray.append(get_humi)
    # print(timeArray, humiArray)
    # get_temp = df['Temperature'].tail(10)
    # tempArray.append(get_temp)
    if n_intervals == 0:
        raise PreventUpdate

    return {
        'data': [go.Scatter(
            x = get_time,
            y = get_humi,
            mode = 'markers+lines',
            line = dict(width = 3, color = '#D35400'),
            marker = dict(size = 7, symbol = 'circle', color = '#D35400',
                          line = dict(color = '#D35400', width = 2)
                          ),

            hoverinfo = 'text',
            hovertext =
            '<b>Time</b>: ' + get_time.astype(str) + '<br>' +
            '<b>Humidity</b>: ' + [f'{x:,.2f}%' for x in get_humi] + '<br>'

        )],

        'layout': go.Layout(
            # paper_bgcolor = 'rgba(0,0,0,0)',
            # plot_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(255, 255, 255, 0.0)',
            paper_bgcolor = 'rgba(255, 255, 255, 0.0)',
            title = {
                'text': '',

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'black',
                'size': 17},

            hovermode = 'closest',
            margin = dict(t = 25, r = 0, l = 40),

            xaxis = dict(range = [min(get_time), max(get_time)],
                         title = '<b>Time</b>',
                         color = 'black',
                         showline = True,
                         showgrid = False,
                         linecolor = 'black',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            yaxis = dict(range = [min(get_humi) - 1, max(get_humi) + 1],
                         title = '<b>Humidity</b>',
                         color = 'black',
                         showline = True,
                         showgrid = True,
                         linecolor = 'black',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'black')

        )

            }


@app.callback(Output('temperature_chart', 'figure'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:sql_root_45t6@localhost:3306/humidity_and_temperature')
    # df = pd.read_sql_table('humiditytemperature', engine)
    # df.to_csv('data.csv')
    # df1 = pd.read_csv('data.csv')
    header_list = ['Time', 'Humidity', 'Temperature']
    df = pd.read_csv('humidity_and_temperature.csv', names = header_list)
    # timeArray = []
    # humiArray = []
    # print(humiArray)
    # tempArray = []
    get_time = df['Time'].tail(20)
    # X = deque(maxlen = 100)
    # timeArray.append(get_time)
    # print(get_time)
    # get_humi = df['Humidity'].tail(10)
    # Y = deque(maxlen = 100)
    # humiArray.append(get_humi)
    # print(get_humi)
    # timeArray.append(get_time)
    # humiArray.append(get_humi)
    # print(timeArray, humiArray)
    get_temp = df['Temperature'].tail(20)
    # tempArray.append(get_temp)
    if n_intervals == 0:
        raise PreventUpdate

    return {
        'data': [go.Scatter(
            x = get_time,
            y = get_temp,
            mode = 'markers+lines',
            line = dict(width = 3, color = '#CA23D5'),
            marker = dict(size = 7, symbol = 'circle', color = '#CA23D5',
                          line = dict(color = '#CA23D5', width = 2)
                          ),

            hoverinfo = 'text',
            hovertext =
            '<b>Time</b>: ' + get_time.astype(str) + '<br>' +
            '<b>Temperature</b>: ' + [f'{x:,.2f}°C' for x in get_temp] + '<br>'

        )],

        'layout': go.Layout(
            plot_bgcolor = 'rgba(255, 255, 255, 0.0)',
            paper_bgcolor = 'rgba(255, 255, 255, 0.0)',
            title = {
                'text': '',

                'y': 0.97,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'black',
                'size': 17},

            hovermode = 'closest',
            margin = dict(t = 25, r = 0, l = 40),

            xaxis = dict(range = [min(get_time), max(get_time)],
                         title = '<b>Time</b>',
                         color = 'black',
                         showline = True,
                         showgrid = False,
                         linecolor = 'black',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            yaxis = dict(range = [min(get_temp) - 0.1, max(get_temp) + 0.1],
                         title = '<b>Temperature</b>',
                         color = 'black',
                         showline = True,
                         showgrid = True,
                         linecolor = 'black',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'black')

        )

            }

@app.callback(Output('text1', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:sql_root_45t6@localhost:3306/humidity_and_temperature')
    # df = pd.read_sql_table('humiditytemperature', engine)
    # df.to_csv('data.csv')
    # df1 = pd.read_csv('data.csv')
    header_list = ['Time', 'Humidity', 'Temperature']
    df = pd.read_csv('humidity_and_temperature.csv', names = header_list)
    # get_time = df['Time'].tail(1).iloc[0].strftime("%Y-%m-%d %H:%M:%S")
    get_time = df['Time'].tail(1).iloc[0]
    get_humi = df['Humidity'].tail(1).iloc[0].astype(float)
    previous_humi = df['Humidity'].tail(2).iloc[0].astype(float)
    change_humidity = get_humi - previous_humi
    # get_temp = df['Temperature'].tail(20)
    if n_intervals == 0:
        raise PreventUpdate

    if change_humidity > 0:

     return [
        html.H6('Humidity',
                style = {'textAlign': 'left',
                         'line-height': '1',
                         'color': '#D35400'}
                ),
        html.P(get_time,
               style = {'textAlign': 'center',
                        'color': 'black',
                        'fontSize': 18,
                        'margin-top': '-3px'
                        }
               ),
        html.P('{0:,.2f}%'.format(get_humi),
               style = {'textAlign': 'center',
                        'color': '#008000',
                        'fontSize': 18,
                        'font-weight': 'bold',
                        'margin-top': '-3px',
                        'line-height': '1',
                        }, className = 'paragraph_value_humi'
               ),
        html.P('+{0:,.2f}%'.format(change_humidity) + ' ' + 'vs previous period',
               style = {'textAlign': 'center',
                        'color': '#008000',
                        'fontSize': 12,
                        'font-weight': 'bold',
                        'margin-top': '-7px',
                        'line-height': '1',
                        }, className = 'change_paragraph_value_humi'
               ),
    ]

    elif change_humidity < 0:

     return [
        html.H6('Humidity',
                style = {'textAlign': 'left',
                         'line-height': '1',
                         'color': '#D35400'}
                ),
        html.P(get_time,
               style = {'textAlign': 'center',
                        'color': 'black',
                        'fontSize': 18,
                        'margin-top': '-3px'
                        }
               ),
        html.P('{0:,.2f}%'.format(get_humi),
               style = {'textAlign': 'center',
                        'color': '#dd1e35',
                        'fontSize': 18,
                        'font-weight': 'bold',
                        'margin-top': '-3px',
                        'line-height': '1',
                        }, className = 'paragraph_value_humi'
               ),
        html.P('{0:,.2f}%'.format(change_humidity) + ' ' + 'vs previous period',
               style = {'textAlign': 'center',
                        'color': '#dd1e35',
                        'fontSize': 12,
                        'font-weight': 'bold',
                        'margin-top': '-7px',
                        'line-height': '1',
                        }, className = 'change_paragraph_value_humi'
               ),
    ]

    elif change_humidity == 0:

     return [
        html.H6('Humidity',
                style = {'textAlign': 'left',
                         'line-height': '1',
                         'color': '#D35400'}
                ),
        html.P(get_time,
               style = {'textAlign': 'center',
                        'color': 'black',
                        'fontSize': 18,
                        'margin-top': '-3px'
                        }
               ),
        html.P('{0:,.2f}%'.format(get_humi),
               style = {'textAlign': 'center',
                        'color': 'black',
                        'fontSize': 18,
                        'font-weight': 'bold',
                        'margin-top': '-3px',
                        'line-height': '1',
                        }, className = 'paragraph_value_humi'
               ),
        html.P('{0:,.2f}%'.format(change_humidity) + ' ' + 'vs previous period',
               style = {'textAlign': 'center',
                        'color': 'black',
                        'fontSize': 12,
                        'font-weight': 'bold',
                        'margin-top': '-7px',
                        'line-height': '1',
                        }, className = 'change_paragraph_value_humi'
               ),
    ]

@app.callback(Output('text2', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:sql_root_45t6@localhost:3306/humidity_and_temperature')
    # df = pd.read_sql_table('humiditytemperature', engine)
    # df.to_csv('data.csv')
    # df1 = pd.read_csv('data.csv')
    header_list = ['Time', 'Humidity', 'Temperature']
    df = pd.read_csv('humidity_and_temperature.csv', names = header_list)
    # get_time = df['Time'].tail(1).iloc[0].strftime("%Y-%m-%d %H:%M:%S")
    get_time = df['Time'].tail(1).iloc[0]
    get_temp = df['Temperature'].tail(1).iloc[0].astype(float)
    previous_temp = df['Temperature'].tail(2).iloc[0].astype(float)
    change_temperature = get_temp - previous_temp
    if n_intervals == 0:
        raise PreventUpdate

    if change_temperature > 0:

        return [
        html.H6('Temperature',
                style = {'textAlign': 'left',
                         'line-height': '1',
                         'color': '#CA23D5'}
                ),
        html.P(get_time,
               style = {'textAlign': 'center',
                        'color': 'black',
                        'fontSize': 18,
                        'margin-top': '-3px'
                        }
               ),
        html.P('{0:,.2f}°C'.format(get_temp),
               style = {'textAlign': 'center',
                        'color': '#008000',
                        'fontSize': 18,
                        'font-weight': 'bold',
                        'margin-top': '-3px',
                        'line-height': '1',
                        }, className = 'paragraph_value_temp'
               ),
        html.P('+{0:,.2f}°C'.format(change_temperature) + ' ' + 'vs previous period',
               style = {'textAlign': 'center',
                        'color': '#008000',
                        'fontSize': 12,
                        'font-weight': 'bold',
                        'margin-top': '-7px',
                        'line-height': '1',
                        }, className = 'change_paragraph_value_temp'
               ),
    ]

    elif change_temperature < 0:
        return [
            html.H6('Temperature',
                    style = {'textAlign': 'left',
                             'line-height': '1',
                             'color': '#CA23D5'}
                    ),
            html.P(get_time,
                   style = {'textAlign': 'center',
                            'color': 'black',
                            'fontSize': 18,
                            'margin-top': '-3px'
                            }
                   ),
            html.P('{0:,.2f}°C'.format(get_temp),
                   style = {'textAlign': 'center',
                            'color': '#dd1e35',
                            'fontSize': 18,
                            'font-weight': 'bold',
                            'margin-top': '-3px',
                            'line-height': '1',
                            }, className = 'paragraph_value_temp'
                   ),
            html.P('{0:,.2f}°C'.format(change_temperature) + ' ' + 'vs previous period',
                   style = {'textAlign': 'center',
                            'color': '#dd1e35',
                            'fontSize': 12,
                            'font-weight': 'bold',
                            'margin-top': '-7px',
                            'line-height': '1',
                            }, className = 'change_paragraph_value_temp'
                   ),
        ]

    elif change_temperature == 0:
        return [
            html.H6('Temperature',
                    style = {'textAlign': 'left',
                             'line-height': '1',
                             'color': '#CA23D5'}
                    ),
            html.P(get_time,
                   style = {'textAlign': 'center',
                            'color': 'black',
                            'fontSize': 18,
                            'margin-top': '-3px'
                            }
                   ),
            html.P('{0:,.2f}°C'.format(get_temp),
                   style = {'textAlign': 'center',
                            'color': 'black',
                            'fontSize': 18,
                            'font-weight': 'bold',
                            'margin-top': '-3px',
                            'line-height': '1',
                            }, className = 'paragraph_value_temp'
                   ),
            html.P('{0:,.2f}°C'.format(change_temperature) + ' ' + 'vs previous period',
                   style = {'textAlign': 'center',
                            'color': 'black',
                            'fontSize': 12,
                            'font-weight': 'bold',
                            'margin-top': '-7px',
                            'line-height': '1',
                            }, className = 'change_paragraph_value_temp'
                   ),
        ]

@app.callback(Output('update', 'children'),
              [Input('update_chart', 'n_intervals')])
def update_graph(n_intervals):
    # engine = sqlalchemy.create_engine('mysql+pymysql://root:sql_root_45t6@localhost:3306/humidity_and_temperature')
    # df = pd.read_sql_table('humiditytemperature', engine)
    header_list = ['Time', 'Humidity', 'Temperature']
    df = pd.read_csv('humidity_and_temperature.csv', names = header_list)
    get_temp = df['Temperature'].tail(1).iloc[0].astype(float)
    if n_intervals == 0:
        raise PreventUpdate

    if get_temp >= 21:
        return [
            html.Div([
                html.H6('Sunny day',
                        style = {'line-height': '1',
                                 'color': '#00FF00'}
                        ),
            html.Img(src=app.get_asset_url('sun.png'),
                     style = {'height': '35px'}),
                ], className = 'temp_card2')
        ]
    elif get_temp < 21:
        return [
            html.Div([
            html.H6('Cloudy day',
                    style = {'line-height': '1',
                             'color': '#00FF00'}
                    ),
            html.Img(src=app.get_asset_url('cloudy-day.png'),
                     style = {'height': '35px'}),
                ], className = 'temp_card2')
        ]



if __name__ == "__main__":
        app.run_server(debug=True)