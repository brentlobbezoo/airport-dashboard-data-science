from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD

from app import app

import math
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import builder

flights = pd.read_csv(os.path.join(os.getcwd(), 'data2-reduced.csv'))

# Encode categorical data
flights['UniqueCarrier'] = LabelEncoder().fit_transform(flights.UniqueCarrier.values)
flights['Origin'] = LabelEncoder().fit_transform(flights.Origin.values)
flights['Dest'] = LabelEncoder().fit_transform(flights.Dest.values)

# Drop unused columns
flights = flights.drop(columns=[
    'Year',
    'FlightNum',
    'TailNum',
    'CancellationCode',
    'DestCoords',
    'OrigCoords',
    'Unnamed: 0',
    'Unnamed: 0.1'
])

# Drop rows with NaN values
flights = flights.dropna()

# Make sure all columns have correct type
flights['Cancelled'] = flights['Cancelled'].astype('bool')

flights['Month'] = flights['Month'].astype('int32')
flights['DayofMonth'] = flights['DayofMonth'].astype('int32')
flights['DayOfWeek'] = flights['DayOfWeek'].astype('int32')
flights['DepTime'] = flights['DepTime'].astype('int32')
flights['CRSDepTime'] = flights['CRSDepTime'].astype('int32')
flights['ArrTime'] = flights['ArrTime'].astype('int32')
flights['CRSArrTime'] = flights['CRSArrTime'].astype('int32')
flights['ActualElapsedTime'] = flights['ActualElapsedTime'].astype('int32')
flights['CRSElapsedTime'] = flights['CRSElapsedTime'].astype('int32')
flights['AirTime'] = flights['AirTime'].astype('int32')
flights['ArrDelay'] = flights['ArrDelay'].astype('int32')
flights['DepDelay'] = flights['DepDelay'].astype('int32')
flights['Distance'] = flights['Distance'].astype('int32')
flights['TaxiIn'] = flights['TaxiIn'].astype('int32')
flights['TaxiOut'] = flights['TaxiOut'].astype('int32')
flights['Diverted'] = flights['Diverted'].astype('int32')
flights['CarrierDelay'] = flights['CarrierDelay'].astype('int32')
flights['WeatherDelay'] = flights['WeatherDelay'].astype('int32')
flights['NASDelay'] = flights['NASDelay'].astype('int32')
flights['SecurityDelay'] = flights['SecurityDelay'].astype('int32')
flights['LateAircraftDelay'] = flights['LateAircraftDelay'].astype('int32')

layout = html.Div(className='row pb-3', children=[
    html.Div(className='col-3', children=[
        builder.build_card(title='Filters', children=[
            html.Form(className='form', children=[
                html.Div(className='mb-3', children=[
                    html.Label(className='form-label', children=[
                        'Normalization method'
                    ]),
                    dcc.Dropdown(
                        id='normalization',
                        options=[
                            { 'label': 'None', 'value': 'none' },
                            { 'label': 'Linear', 'value': 'linear' },
                            # { 'label': 'Square root', 'value': 'square' },
                            # { 'label': 'Log', 'value': 'log' },
                        ],
                        value='none',
                        className='dcc_control',
                        clearable=False
                    ),
                ]),
                html.Div(className='mb-3', children=[
                    html.Label(className='form-label', children=[
                        'Feature reduction method'
                    ]),
                    dcc.Dropdown(
                        id='method',
                        options=[
                            { 'label': 'PCA', 'value': 'PCA' },
                            { 'label': 'SVD', 'value': 'SVD' },
                        ],
                        value='PCA',
                        className='dcc_control',
                        clearable=False
                    ),
                ])
            ])
        ])
    ]),
    html.Div(className='col-9', children=[
        builder.build_card(title='Components 3D-scatter plot', children=[
            dcc.Graph(id='decomposition'),
            html.P(id='variance', className='mt-3')
        ]),
    ]),
])

# Functions
def linear_normalization(val, min_val, max_val):
    """
    Returns the linear normalization value
    """
    val = (val - min_val) / (max_val - min_val)

    if math.isnan(val):
        return 0

    return val

def square_root_normalization(val, min_val, max_val):
    """
    Returns the square root normalization value
    """
    return (math.sqrt(val) - math.sqrt(min_val)) / (math.sqrt(max_val) - math.sqrt(min_val))

def logarithmic_normalization(val, min_val, max_val):
    """
    Returns the log normalization value
    """
    return (math.log(val) - math.log(min_val)) / (math.log(max_val) - math.log(min_val))

def normalize_column(df, column, method=linear_normalization):
    """
    Uses the linear normalization formula on a given column in a DataFrame
    """
    min_val = df[column].min()
    max_val = df[column].max()

    val = df[column].apply(lambda val: method(val, min_val, max_val))
    df[column] = val
    
    return df

def normalize(df, columns, method=linear_normalization):
    """
    Calls the normalization function for each provided column from
    the given DataFrame
    """
    for column in columns:
        df = normalize_column(df, column, method)
    
    return df

# Callbacks
@app.callback(
    Output(component_id='decomposition', component_property='figure'),
    Output(component_id='variance', component_property='children'),
    Input(component_id='method', component_property='value'),
    Input(component_id='normalization', component_property='value'),
)
def decomposition(method=None, normalization=None):
    '''
    Returns a plotly figure, showing a scatter plot between two variables.
    '''
    flights_copy = flights.copy()
    flights_copy = flights_copy.reset_index()

    columns = [
        'Month', 
        'DayofMonth', 
        'DayOfWeek', 
        'DepTime', 
        'CRSDepTime', 
        'ArrTime', 
        'CRSArrTime', 
        'ActualElapsedTime', 
        'CRSElapsedTime', 
        'AirTime', 
        'ArrDelay', 
        'DepDelay', 
        'Distance', 
        'TaxiIn', 
        'TaxiOut', 
        'CarrierDelay', 
        'WeatherDelay', 
        'NASDelay', 
        'SecurityDelay', 
        'LateAircraftDelay'
    ]

    if normalization == 'linear':
        flights_copy = normalize(flights_copy, columns, linear_normalization)
    elif normalization == 'square':
        flights_copy = normalize(flights_copy, columns, square_root_normalization)
    elif normalization == 'log':
        flights_copy = normalize(flights_copy, columns, logarithmic_normalization)

    decomposition = PCA(n_components=3)

    if method == 'SVD':
        decomposition = TruncatedSVD(n_components=3)

    features = [col for col in flights_copy]
    features.remove('Cancelled')
    components = decomposition.fit_transform(flights_copy[features])
    components_df = pd.DataFrame(components, columns=['Component 1', 'Component 2', 'Component 3'])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=components_df['Component 1'],
            y=components_df['Component 2'],
            z=components_df['Component 3'],
            mode='markers',
            marker=dict(
                size=1
            )
        )
    )

    fig.update_layout(
        height=500,
        margin={ 'r': 0, 't': 0, 'l': 0, 'b': 0},
    )

    variance = decomposition.explained_variance_ratio_.sum() * 100
    variance = 'Explained variance: ({:.2f}%)'.format(variance)

    return fig, variance