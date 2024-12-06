import json
import pandas as pd
import dash
from dash import dcc
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from waitress import serve
import requests
import time
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function, assign
from .tools import *


def forecaster(tags, api_key, weather=None, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        fcst_dict = {}
        for tag in tags:
            df = tags[tag]
            if weather is not None:
                lat = weather['lat']
                lon = weather['lon']
            else:
                lat = None
                lon = None
            x = requests.post('https://www.waterworks.ai/api/forecast',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'api_key': api_key, 'lat': lat,
                                    'lon': lon})
            js = x.json()
            # fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            fcst_dict[tag] = fcst

        return fcst_dict
    else:
        app = dash.Dash(__name__,
                        title='Forecasting',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )

        #saved_figures = [f for f in os.listdir(output_dir) if f.endswith('.json')]
        #options = [{'label': os.path.splitext(f)[0], 'value': f} for f in saved_figures]

        # initial_figure = from_json(initial_figure_path)

        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Forecasting', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             # dbc.Container(buttons, style={'text-align':'center'})
             dbc.Row(html.P('Select flow series below.',
                            style={"text-align": "center"}, className='lead')),
             dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown', options=[{'label': t, 'value': t} for t in tags])), style={'width':'30%'}),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='forecast-plot')))
             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])


        @app.callback(
            Output('forecast-plot', 'figure'),
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            df = tags[tag]
            if weather is not None:
                lat = weather['lat']
                lon = weather['lon']
            else:
                lat = None
                lon = None
            x = requests.post('https://www.waterworks.ai/api/forecast', json={'df':df.to_json(orient='records', date_format='iso'), 'api_key':api_key, 'lat':lat, 'lon':lon})
            js = x.json()
            #fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            df = df.iloc[-10*fcst.shape[0]:]
            trace = go.Scatter(
                name='Past flow',
                mode='lines',
                x=list(df['ds']),
                y=list(df['y']),
                marker=dict(
                    color='grey',
                    line=dict(width=1)
                )
            )
            trace1 = go.Scatter(
                name='Forecast',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['yhat']),
                marker=dict(
                    color='#ed729d',
                    line=dict(width=1)
                )
            )
            upper_band = go.Scatter(
                name='Upper band',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['hi-90']),
                line=dict(color='#A7C7E7'),
                fill='tonexty'
            )
            lower_band = go.Scatter(
                name='Lower band',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['lo-90']),
                line=dict(color='#A7C7E7')
            )
            data = [trace, lower_band, upper_band, trace1]

            layout = dict(title=tag+' Forecast',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)
            return fig

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def leak_detector(tags, api_key, unit, night_mode=False, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        leak_list = []
        for tag in tags:
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/leakage',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'unit': unit, 'night_mode':night_mode,
                                    'api_key': api_key})
            js = x.json()
            # fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            df['ds'] = pd.to_datetime(df['ds'])
            fcst['ds'] = pd.to_datetime(fcst['ds'])
            df = df.set_index('ds')
            fcst = fcst.set_index('ds')
            df['Alarm'] = fcst['anomaly']
            active = fcst.iloc[-3:]['anomaly'].sum()

            if active > 0:
                leak_list.append(tag)
            else:
                pass
            time.sleep(1)

        return leak_list
    else:
        app = dash.Dash(__name__,
                        title='Leak Detector',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )



        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Leak Detector', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             dbc.Row(html.P('Any identified leaks will be listed below.',
                            style={"text-align": "center"}, className='lead')),
             # dbc.Container(buttons, style={'text-align':'center'})
             dcc.Loading(id='loading', children=dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown')), style={'width':'30%'})),
             html.Br(),
             dbc.Row(html.P('Flow & Alarm',
                            style={"text-align": "center", 'font-weight': 'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='anomaly-plot')))
             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])

        @app.callback(
            Output('tag-dropdown', 'options'),
            Input('url','pathname')
        )
        def loop(pathname):
            import plotly.graph_objs as go
            options = []
            for tag in tags:
                df = tags[tag]
                x = requests.post('https://www.waterworks.ai/api/leakage', json={'df': df.to_json(orient='records', date_format='iso'), 'unit':unit, 'night_mode':night_mode, 'api_key':api_key})
                js = x.json()
                # fig = plotly.io.from_json(json.dumps(js))
                fcst = pd.read_json(json.dumps(js), orient='records')
                df['ds'] = pd.to_datetime(df['ds'])
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                df = df.set_index('ds')
                fcst = fcst.set_index('ds')
                df['Alarm'] = fcst['anomaly']
                active = fcst.iloc[-3:]['anomaly'].sum()

                df.loc[df['Alarm'] == 1, 'Alarm'] = df['y']
                df.loc[df['Alarm'] == 0, 'Alarm'] = None
                print('here', fcst['anomaly'])
                df = df.reset_index()
                if active > 0:
                    options.append({'label': tag, 'value': df.to_json(orient='records',date_format='iso')})
                else:
                    pass
                time.sleep(1)

            return options


        @app.callback(
            Output('anomaly-plot', 'figure'),
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            print(tag)
            df = pd.read_json(tag, orient='records')
            df = df.reset_index()


            trace = go.Scatter(
                name='Past flow',
                mode='lines',
                x=list(df['ds']),
                y=list(df['y']),
                marker=dict(
                    color='grey',
                    line=dict(width=1)
                )
            )

            anomaly = go.Scatter(
                name='Alarm',
                mode='markers',
                x=list(df['ds']),
                y=list(df['Alarm']),
                line=dict(color='red'),
            )

            data = [trace, anomaly]

            layout = dict(title='Potential Leaks',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)
            return fig

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def blockage_detector(tags, api_key, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        blockage_list = []
        for tag in tags:
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/blockage',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'api_key': api_key})
            js = x.json()
            # fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            df['ds'] = pd.to_datetime(df['ds'])
            fcst['ds'] = pd.to_datetime(fcst['ds'])
            df = df.set_index('ds')
            fcst = fcst.set_index('ds')
            df['Alarm'] = fcst['anomaly']
            active = fcst.iloc[-3:]['anomaly'].sum()

            if active > 0:
                blockage_list.append(tag)
            else:
                pass
            time.sleep(1)

        return blockage_list
    else:
        app = dash.Dash(__name__,
                        title='Blockage Detector',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )

        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Blockage Detector', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             dbc.Row(html.P('Any identified blockages will be listed below.',
                            style={"text-align": "center"}, className='lead')),
             dcc.Loading(id='loading',
                         children=dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown')), style={'width': '30%'})),
             html.Br(),
             dbc.Row(html.P('Flow & Alarm',
                            style={"text-align": "center", 'font-weight': 'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='anomaly-plot')))
             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])

        @app.callback(
            Output('tag-dropdown', 'options'),
            Input('url', 'pathname')
        )
        def loop(pathname):
            import plotly.graph_objs as go
            options = []
            for tag in tags:
                df = tags[tag]
                x = requests.post('https://www.waterworks.ai/api/blockage',
                                  json={'df': df.to_json(orient='records', date_format='iso'), 'api_key':api_key})
                js = x.json()
                # fig = plotly.io.from_json(json.dumps(js))
                fcst = pd.read_json(json.dumps(js), orient='records')
                df['ds'] = pd.to_datetime(df['ds'])
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                df = df.set_index('ds')
                fcst = fcst.set_index('ds')
                df['Alarm'] = fcst['anomaly']
                active = fcst.iloc[-3:]['anomaly'].sum()
                df.loc[df['Alarm'] == 1, 'Alarm'] = df['y']
                df.loc[df['Alarm'] == 0, 'Alarm'] = None
                print('here', fcst['anomaly'])
                df = df.reset_index()
                if active > 0:
                    options.append({'label': tag, 'value': df.to_json(orient='records', date_format='iso')})
                else:
                    pass
                time.sleep(1)

            return options

        @app.callback(
            Output('anomaly-plot', 'figure'),
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            print(tag)
            df = pd.read_json(tag, orient='records')
            df = df.reset_index()

            trace = go.Scatter(
                name='Past flow',
                mode='lines',
                x=list(df['ds']),
                y=list(df['y']),
                marker=dict(
                    color='grey',
                    line=dict(width=1)
                )
            )

            anomaly = go.Scatter(
                name='Alarm',
                mode='markers',
                x=list(df['ds']),
                y=list(df['Alarm']),
                line=dict(color='red'),
            )

            data = [trace, anomaly]

            layout = dict(title='Potential Blockages',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)
            return fig

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def inflow_infiltration(tags, api_key, person_equivalents=None, snowmelt=False, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        inflow_infil_dict = {}
        for tag in tags:
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/inflow',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'api_key': api_key})
            js = x.json()
            fcst = pd.read_json(json.dumps(js), orient='records')

            if person_equivalents is not None:
                unit = person_equivalents[tag]['unit']
                population = person_equivalents[tag]['population']
                personal_daily_volume = person_equivalents[tag]['personal_daily_volume']
                u = unit.split('/')[-1]
                if u == 's':
                    vol = (population * personal_daily_volume) / 86400
                elif u == 'h':
                    vol = (population * personal_daily_volume) / 24
                elif u == 'd':
                    vol = population * personal_daily_volume
                share = vol / fcst['DWF'].mean()

                fcst['Usage'] = share * fcst['DWF']
                fcst['BF'] = fcst['DWF'] - fcst['Usage']

                inflow_infil_dict[tag] = {'total':fcst['y'].sum(),'inflow':fcst['y'].sum() - fcst['DWF'].sum(),'sewage':fcst['DWF'].sum() - fcst['BF'].sum(),
                                          'infiltration':fcst['BF'].sum()}

            else:
                inflow_infil_dict[tag] = {'total': fcst['y'].sum(), 'inflow': fcst['y'].sum() - fcst['DWF'].sum(),
                                          'dwf': fcst['DWF'].sum()}
            if snowmelt is True:
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                fcst['month'] = fcst.ds.dt.month
                fcst_summer = fcst.loc[fcst['month'].isin([5, 6, 7, 8, 9, 10])]
                fcst_winter = fcst.loc[fcst['month'].isin([11, 12, 1, 2, 3, 4])]
                inflow_infil_dict['inflow_rainfall'] = fcst_summer['y'].sum() - fcst_summer['DWF'].sum()
                inflow_infil_dict['inflow_snowmelt'] = fcst_winter['y'].sum() - fcst_winter['DWF'].sum()

        return inflow_infil_dict
    else:
        app = dash.Dash(__name__,
                        title='Inflow & Infiltration',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )


        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Inflow & Infiltration', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             # dbc.Container(buttons, style={'text-align':'center'})
             dbc.Row(html.P('Select flow series below.',
                            style={"text-align": "center"}, className='lead')),
             dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown', options=[{'label': t, 'value': t} for t in tags])), style={'width':'30%'}),
             html.Br(),
             dbc.Row(html.P('Flow composition over time',
                            style={"text-align": "center", 'font-weight':'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='anomaly-plot'))),
             html.Br(),
             dbc.Row(html.P('Flow totals',
                            style={"text-align": "center", 'font-weight':'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='volume-plot'))),
             html.Div(id='snowmelt-div')

             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])


        @app.callback(
            [Output('anomaly-plot', 'figure'), Output('volume-plot','figure'), Output('snowmelt-div', 'children')],
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            import plotly.express as px
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/inflow', json={'df':df.to_json(orient='records', date_format='iso'), 'api_key':api_key})
            js = x.json()
            fcst = pd.read_json(json.dumps(js), orient='records')

            if person_equivalents is not None:
                unit = person_equivalents[tag]['unit']
                population = person_equivalents[tag]['population']
                personal_daily_volume = person_equivalents[tag]['personal_daily_volume']
                u = unit.split('/')[-1]
                if u == 's':
                    vol = (population * personal_daily_volume) / 86400
                elif u == 'h':
                    vol = (population * personal_daily_volume) / 24
                elif u == 'd':
                    vol = population * personal_daily_volume
                share = vol / fcst['DWF'].mean()

                fcst['Usage'] = share * fcst['DWF']
                fcst['BF'] = fcst['DWF'] - fcst['Usage']

                inflow = go.Scatter(
                    name='Inflow',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['y']),
                    marker=dict(
                        color='#4C78A8',
                        # line=dict(width=1)
                    ),
                    fill='tonexty'

                )
                sewage = go.Scatter(
                    name='Sewage',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['DWF']),
                    line=dict(color='#E45756'),
                    fill='tonexty'

                )
                infiltration = go.Scatter(
                name='Infiltration',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['BF']),
                line=dict(color='#9D755D'),
                fill='tozeroy'

            )


                vol = pd.DataFrame()
                vol['Type'] = ['Inflow', 'Sewage', 'Infiltration']
                vol['Volume'] = [fcst['y'].sum() - fcst['DWF'].sum(), fcst['DWF'].sum()-fcst['BF'].sum(), fcst['BF'].sum()]
                data = [infiltration, sewage, inflow]
            else:
                inflow = go.Scatter(
                    name='Inflow',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['y']),
                    line=dict(color='#4C78A8'),

                    fill='tonexty'

                )

                dwf = go.Scatter(
                    name='Sewage',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['DWF']),
                    line=dict(color='#E45756'),
                    fill='tozeroy'

                )
                vol = pd.DataFrame()
                vol['Type'] = ['Inflow', 'Sewage']
                vol['Volume'] = [fcst['y'].sum() - fcst['DWF'].sum(), fcst['DWF'].sum()]

                data = [dwf, inflow]


            layout = dict(title='Inflow',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)


            vol_fig = px.pie(vol, values='Volume', names='Type', color='Type', color_discrete_map={'Inflow':'#4C78A8',
                                     'Sewage':'#E45756',
                                     'Infiltration':'#9D755D'})
            if snowmelt is True:
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                fcst['month'] = fcst.ds.dt.month
                fcst_summer = fcst.loc[fcst['month'].isin([5, 6, 7, 8, 9, 10])]
                fcst_winter = fcst.loc[fcst['month'].isin([11, 12, 1, 2, 3, 4])]

                season = pd.DataFrame()
                season['Inflow Type'] = ['Rainfall', 'Snowmelt']
                season['Volume'] = [fcst_summer['y'].sum() - fcst_summer['DWF'].sum(),
                                    fcst_winter['y'].sum() - fcst_winter['DWF'].sum()]

                season_fig = px.bar(season, x='Inflow Type', y='Volume', color='Inflow Type',
                                    color_discrete_map={'Rainfall': '#4C78A8',
                                                        'Snowmelt': '#4C78A8'})
                season_fig.update_layout(
                    plot_bgcolor='white'
                )

                snowmelt_div = [html.Br(),
                                dbc.Row(html.P('Rainfall vs Snowmelt',
                                               style={"text-align": "center", 'font-weight': 'bold'},
                                               className='lead')),
                                html.Br(),
                                dbc.Container(dbc.Row(dcc.Graph(figure=season_fig)))]
            else:
                snowmelt_div = []

            return fig, vol_fig, snowmelt_div

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def pipe_network(pipe_gdf, api_key, id_col=None, construction_col=None, renovation_col=None, material_col=None, dimension_col=None, length_col=None, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        pass
    else:
        pipes = PipeNetwork(pipe_gdf)
        gdf_lof = pipes.get_lof(api_key, id_col, construction_col, renovation_col, material_col, dimension_col, length_col)
        gdf_cof = pipes.get_cof(api_key, id_col, dimension_col)
        gdf_rof = pipes.get_rof(gdf_lof, gdf_cof, id_col)
        app = dash.Dash(__name__,
                        title='Pipe Network',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )

        style_handle = {
            "variable": "dashExtensions.default.styleHandle"
        }

        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Pipe Network', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),

             dbc.Container(dbc.Row(html.Div(
                 [
                     dbc.Label("Choose Metric to Plot"),
                     dbc.RadioItems(
                         id="select",
                         options=[
                             {"label": "Condition", "value": "LoF"},
                             {"label": "Consequence", "value": "CoF"},
                             {"label": "Risk", "value": "RoF"},
                         ],
                         value='LoF',
                         inline=True,
                     ),
                 ]
             )), style={'text-align': 'center'}),
             html.Br(),

             dbc.Container(dbc.Row(html.Div(id='pipe-map'))),
             html.Br(),
             dbc.Row(html.H3('Renewal Need',
                             style={"text-align": "center"}, className='lead')),
             html.Br(),
             dbc.Row(html.P('Simulates annual renewal need (km pipe) per material, based on a set renewal rate (%).',
                            style={"text-align": "center"}, className='lead')),
             dbc.Container(dbc.Row(html.Div(
                 [
                     dbc.Label("Set Yearly Renewal Rate (%)", html_for="slider"),
                     dcc.Slider(id="slider", min=0, max=5, step=0.5, value=0),
                 ]
             ))),
             dbc.Container(dbc.Row(dcc.Graph(id='renewal-chart'))),
             html.Br(),
             dbc.Row(html.H3('5-Year Plan',
                             style={"text-align": "center"})),
             dbc.Row(html.P('These are the pipes that should be prioritized for renewal, '
                            'based on the set renewal rate and the estimated risk of failure (RoF).',
                            style={"text-align": "center"}, className='lead')),
             dbc.Container(dbc.Row(dash_table.DataTable(id='pipe-table', style_table={
                 'overflowY': 'scroll',
                 'height': '250px',
             }, style_as_list_view=True))),

             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])

        @app.callback(
            Output('pipe-map', 'children'),
            [Input('select', 'value')],
        )
        def update_map(tag):
            clr = tag
            gdf = gdf_rof.copy()
            gjs = eval(gdf[[id_col, clr, 'geometry']].to_json())
            classes = [round(gdf[clr].min(), 1), round(((gdf[clr].max() - gdf[clr].min()) / 7), 1),
                       round(2 * ((gdf[clr].max() - gdf[clr].min()) / 7), 1),
                       round(3 * ((gdf[clr].max() - gdf[clr].min()) / 7), 1),
                       round(4 * ((gdf[clr].max() - gdf[clr].min()) / 7), 1),
                       round(5 * ((gdf[clr].max() - gdf[clr].min()) / 7), 1),
                       round(6 * ((gdf[clr].max() - gdf[clr].min()) / 7), 1),
                       round(gdf[clr].max(), 1)]
            colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']

            style = dict(weight=3, opacity=1, dashArray='3', fillOpacity=0.7)
            # Create colorbar.
            ctg = ["{}".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}".format(classes[-1])]
            colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30,
                                                position="bottomleft")
            # Geojson rendering logic, must be JavaScript as it is executed in clientside.

            # Create geojson.
            geojson = dl.GeoJSON(data=gjs,  # url to geojson file
                                 style=style_handle,  # how to style each polygon
                                 zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                                 zoomToBoundsOnClick=True,
                                 # when true, zooms to bounds of feature (e.g. polygon) on click
                                 hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),
                                 # style applied on hover
                                 hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp=clr),
                                 id="geojson")
            # Create info control.
            info = dbc.Card(id="info", className="info",
                            style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"})
            # Create app.
            children = dl.Map(children=[
                dl.TileLayer(
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                    attribution=(
                        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors '
                        '&copy; <a href="https://carto.com/">CARTO</a>'
                    )
                ), geojson, colorbar, info
            ], style={'height': '80vh'}, center=[56, 10], zoom=6)  # dl.TileLayer() for osm

            return children

        @app.callback(Output("info", "children"),
                      [Input('select', 'value'), Input("geojson", "hoverData")])
        def info_hover(tag, feature):
            clr = tag

            def get_info(feature=None):
                header = [html.P("Pipe Info", style={'font-weight':'bold'})]
                print(feature)
                if not feature:
                    return header + [html.P("Hover over a pipe")]
                return header + [html.B(feature["properties"][id_col]), html.Br(),
                                 str(clr)+" = {}".format(feature["properties"][clr])]

            return get_info(feature)

        @app.callback([Output('renewal-chart', 'figure'),
                       Output('pipe-table', 'data'), Output('pipe-table', 'columns')],
                      Input('slider', 'value'))
        def renewal(renewal_rate):
            import plotly.express as px

            df_all, five_year_plan = pipes.get_renewal_need(renewal_rate, gdf_lof, gdf_rof, id_col, material_col, length_col)
            fig = px.area(df_all, x='Year', y='Renewal Need (km)', color='Material')
            five_year_plan = five_year_plan.drop(['geometry'], axis=1)

            return fig, five_year_plan.to_dict('records'), [{"name": i, "id": i} for i in five_year_plan.columns]

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)