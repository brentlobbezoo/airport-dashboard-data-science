from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px

from app import app, df
from utils import builder
from utils import modifier

options = [
    { 'label': 'ArrDelay', 'value': 'ArrDelay' },
    { 'label': 'CarrierDelay', 'value': 'CarrierDelay' },
    { 'label': 'LateAircraftDelay', 'value': 'LateAircraftDelay' },
    { 'label': 'NASDelay', 'value': 'NASDelay' },
    { 'label': 'WeatherDelay', 'value': 'WeatherDelay' }
]

layout = html.Div(className='row pb-3', children=[
    html.Div(className='col-3', children=[
        builder.build_card(title='Filters', children=[
            html.P(className='text-muted', children=[
                'This page allows you to compare the relation between the different delay features. Note that feature 1 will be plotted along the x-axis. Feature 2 will be plotted along the y-axis.'
            ]),
            html.Form(className='form', children=[
                html.Div(className='mb-3', children=[
                    html.Label(className='form-label', children=[
                        'Feature 1'
                    ]),
                    dcc.Dropdown(
                        id='feature-1',
                        options=options,
                        value=options[0]['value'],
                        className='dcc_control',
                        clearable=False
                    ),
                ]),
                html.Div(className='mb-3', children=[
                    html.Label(className='form-label', children=[
                        'Feature 2'
                    ]),
                    dcc.Dropdown(
                        id='feature-2',
                        options=options,
                        value=options[1]['value'],
                        className='dcc_control',
                        clearable=False
                    ),
                ]),
            ])
        ])
    ]),
    html.Div(className='col-9', children=[
        builder.build_card(title='Scatter plot', children=[
            dcc.Graph(id='scatter')
        ])
    ]),
])

# Callbacks
@app.callback(
    Output(component_id='scatter', component_property='figure'),
    Input(component_id='feature-1', component_property='value'),
    Input(component_id='feature-2', component_property='value'),
)
def scatter(feature_1=None, feature_2=None):
    '''
    Returns a plotly figure, showing a scatter plot between two variables.
    '''
    if not feature_1:
        feature_1 = options[0]['value']

    if not feature_2:
        feature_2 = options[1]['value']

    df_copy = df.copy()

    return px.scatter(df_copy, x=feature_1, y=feature_2)