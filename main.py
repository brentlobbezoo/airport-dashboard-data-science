import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

from datetime import date
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from builder import build_card
from utils import filter_df
from controls import MONTHS

app = dash.Dash(__name__)

# Handling DataFrame
df = pd.read_csv(os.path.join(os.getcwd(), 'data.csv'))

df['Date'] = pd.to_datetime(df.Month.astype(str) + '/' + df.DayofMonth.astype(str) + '/' + df.Year.astype(str))
# df['Date']= pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df.drop(columns=['Year', 'Month', 'DayofMonth'])

# Extending controls
destinations = pd.unique(df['Dest'].values.ravel())
origins = pd.unique(df['Origin'].values.ravel())

destinations.sort()
origins.sort()

DESTINATIONS = list(map(lambda x: { 'label': x, 'value': x }, destinations))
ORIGINS = list(map(lambda x: { 'label': x, 'value': x }, origins))

# Callbacks
@app.callback(
    Output(component_id='flights-per-month', component_property='figure'),
    Input(component_id='months', component_property='value'),
    Input(component_id='origin', component_property='value'),
    Input(component_id='destination', component_property='value')
)
def flights_per_month(months=None, origins=None, destinations=None):
    '''
    Returns a plotly figure, showing the amount of flights per month.
    '''
    df_copy = df.copy()

    flights = filter_df(df_copy, months=months, origins=origins, destinations=destinations)
    flights = flights['Date'].value_counts().reset_index()

    return px.bar(flights, x='index', y='Date', labels={
        'index': 'Months',
        'Date': 'Amount of flights',
    })

@app.callback(
    Output(component_id='delayed-flights', component_property='figure'),
    Input(component_id='months', component_property='value'),
    Input(component_id='origin', component_property='value'),
    Input(component_id='destination', component_property='value')
)
def delayed_flights(months=None, origins=None, destinations=None):
    '''
    Returns a plotly figure, showing the amount of flights per month.
    '''
    df_copy = df.copy()

    flights = filter_df(df_copy, months=months, origins=origins, destinations=destinations)
    flights = flights['Date'].value_counts().reset_index()

    return px.bar(flights, x='index', y='Date', labels={
        'index': 'Months',
        'Date': 'Amount of flights',
    })

# Rendering the layout
app.layout = html.Div(className='container p-3', children=[
    html.Div(className='row pb-3', children=[
        html.Div(className='col-3', children=[
            build_card(title='Filters', children=[
                html.Form(className='form', children=[
                    html.Div(className='mb-3', children=[
                        html.Label(className='form-label', children=[
                            'Months'
                        ]),
                        dcc.Dropdown(
                            id='months',
                            options=MONTHS,
                            multi=True,
                            className='dcc_control'
                        ),
                    ]),
                    html.Div(className='mb-3', children=[
                        html.Label(className='form-label', children=[
                            'Flight origin'
                        ]),
                        dcc.Dropdown(
                            id='origin',
                            options=ORIGINS,
                            multi=True,
                            className='dcc_control'
                        ),
                    ]),
                    html.Div(className='mb-3', children=[
                        html.Label(className='form-label', children=[
                            'Flight destination'
                        ]),
                        dcc.Dropdown(
                            id='destination',
                            options=DESTINATIONS,
                            multi=True,
                            className='dcc_control'
                        ),
                    ])
                ])
            ])
        ]),
        html.Div(className='col-9', children=[
            build_card(title='Flights per month', children=[
                dcc.Graph(id='flights-per-month')
            ])
        ]),
    ]),
    html.Div(className='row pb-3', children=[
        html.Div(className='col-6', children=[
            build_card(title='Delayed flights', children=[
                dcc.Graph(id='delayed-flights')
            ])
        ]),
        html.Div(className='col-6', children=[
            build_card(title='Map', children=[

            ])
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)