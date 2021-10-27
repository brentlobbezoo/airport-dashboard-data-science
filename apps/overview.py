from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app import app, df, airports, DESTINATIONS, ORIGINS, CARRIERS
from utils import builder
from utils import controls
from utils import modifier

# Overview layout
layout = [
    html.Div(className='row pb-3', children=[
        html.Div(className='col-3', children=[
            builder.build_card(title='Filters', children=[
                html.Form(className='form', children=[
                    html.Div(className='mb-3', children=[
                        html.Label(className='form-label', children=[
                            'Months'
                        ]),
                        dcc.Dropdown(
                            id='months',
                            options=controls.MONTHS,
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
            builder.build_card(title='Flights per month', children=[
                dcc.Graph(id='flights-per-month')
            ])
        ]),
    ]),
    html.Div(className='row pb-3', children=[
        html.Div(className='col-6', children=[
            builder.build_card(title='Flight statusses', children=[
                dcc.Graph(id='delayed-flights')
            ])
        ]),
        html.Div(className='col-6', children=[
            builder.build_card(title='Lorem ipsum', children=[

            ])
        ])
    ]),
    html.Div(className='row pb-3', children=[
        html.Div(className='col-12', children=[
            builder.build_card(title='Map', children=[
                dcc.Graph(id='map', style={ 'width': '100%', 'height': '700' })
            ], footer=[
                html.P(className='text-muted', children=[
                    'The map requires some extra parameters (a specific date and carrier) due to the large amount of flights. Being able to show all the flights in a certain month, would likely cause the application to run very slow. Please wait a moment for the results to show.'
                ]),
                html.Form(className='form', children=[
                    html.Div(className='row', children=[
                        html.Div(className='col', children=[
                            dcc.DatePickerSingle(
                                id='date',
                                min_date_allowed=date(2008, 1, 1),
                                max_date_allowed=date(2008, 12, 31),
                                initial_visible_month=date(2008, 1, 1),
                                date=date(2008, 1, 1),
                                className='datepicker'
                            ),
                        ]),
                        html.Div(className='col', children=[
                            dcc.Dropdown(
                                id='carrier',
                                placeholder='Carrier',
                                value=CARRIERS[0]['value'],
                                options=CARRIERS,
                                multi=False,
                                className='dcc_control',
                                clearable=False
                            ),
                        ])
                    ]),
                ])
            ])
        ])
    ])
]

# Callbacks
@app.callback(
    Output(component_id='flights-per-month', component_property='figure'),
    Input(component_id='months', component_property='value'),
    Input(component_id='origin', component_property='value'),
    Input(component_id='destination', component_property='value'),
)
def flights_per_month(months=None, origins=None, destinations=None):
    '''
    Returns a plotly figure, showing the amount of flights per month.
    '''
    df_copy = df.copy()

    flights = modifier.filter_df(df_copy, months=months, origins=origins, destinations=destinations)
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
    Returns a plotly figure, showing the statusses.
    '''
    df_copy = df.copy()

    flights = modifier.filter_df(df_copy, months=months, origins=origins, destinations=destinations)
    flights = flights['Status'].value_counts().reset_index()

    return px.pie(flights, values='Status', names='index', labels={
        'index': 'Status',
        'Status': 'Amount',
    })

@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='months', component_property='value'),
    Input(component_id='origin', component_property='value'),
    Input(component_id='destination', component_property='value'),
    Input(component_id='carrier',  component_property='value'),
    Input(component_id='date',  component_property='date')
)
def flights_map(months=None, origins=None, destinations=None, carrier=None, date_value=None):
    '''
    Returns a plotly figure, showing a map of flights.
    '''
    if not carrier or not date_value:
        return 'Please provide a carrier and date value'

    # Parse date parameter
    date_value = date.fromisoformat(date_value)
    date_value = date_value.strftime('%m/%d/%Y')

    df_copy = df.copy()

    # Filter flights
    flights = modifier.filter_df(df_copy, months=months, origins=origins, destinations=destinations)
    flights = flights[flights.UniqueCarrier == carrier]
    flights = flights[flights.Date == date_value]

    # Find unique AITA codes
    unique_aita = pd.unique(flights[['Origin', 'Dest']].values.ravel())

    # Initalize figure
    fig = go.Figure()

    # Fetch only airports with needed AITA codes
    airports_copy = airports[airports.code.isin(unique_aita)]
    
    if not airports_copy.empty:
        airports_copy[['lon', 'lat']] = airports_copy['coordinates'].str.split(';', expand=True)

        # Add all airports as a marker if there are any
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=airports_copy['lon'],
            lat=airports_copy['lat'],
            hoverinfo='text',
            text=airports_copy['code'],
            mode='markers',
            marker=dict(color='red')
        ))
    else:
        # Add random "fake" trace to render map
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[0],
            lat=[0],
            mode='markers',
            marker=dict(color='red')
        ))

    # Modify flights to get a count of each unique flight-path
    flights = flights.groupby(['OrigCoords', 'DestCoords']).size().reset_index().rename(columns={ 0: 'count'})
    max_value = flights['count'].max()

    # Add all flight paths to the figure
    for index, row in flights.iterrows():
        start_lon, start_lat = row['OrigCoords'].split(';')
        end_lon, end_lat = row['DestCoords'].split(';')

        fig.add_trace(
            go.Scattergeo(
                locationmode='USA-states',
                lon=[float(start_lon), float(end_lon)],
                lat=[float(start_lat), float(end_lat)],
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=float(row['count']) / float(max_value)
            )
        )

    # Set map layout
    fig.update_layout(
        height=500,
        showlegend=False,
        margin={ 'r': 0, 't': 0, 'l': 0, 'b': 0},
        geo=dict(
            scope='north america',
            projection_type='azimuthal equal area',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            framewidth=100
        )
    )

    return fig
