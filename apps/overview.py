from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from app import app, df, airports, DESTINATIONS, ORIGINS
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
                dcc.Graph(id='map',style={ 'width': '100%', 'height': '500px' })
            ], footer=[

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
    Input(component_id='destination', component_property='value')
)
def flights_map(months=None, origins=None, destinations=None):
    '''
    Returns a plotly figure, showing a map of flights.
    '''
    df_copy = df.copy()

    flights = modifier.filter_df(df_copy, months=months, origins=origins, destinations=destinations)
    flights = flights[flights.Date == '01/01/2008']

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=airports['coordinates'].str.split(';')[0],
        lat=airports['coordinates'].str.split(';')[1],
        hoverinfo='text',
        text=airports['code'],
        mode='markers',
        marker=dict(
            size=2,
            color='rgb(255, 0, 0)',
            line=dict(
                width=3,
                color='rgba(68, 68, 68, 0)'
            )
        ))
    )

    for index, row in flights.iterrows():
        start_lon, start_lat = row['OrigCoords'].split(';')
        end_lon, end_lat = row['DestCoords'].split(';')

        fig.add_trace(
            go.Scattergeo(
                locationmode='USA-states',
                lon=[float(start_lon), float(end_lon)],
                lat=[float(start_lat), float(end_lat)],
                mode='lines+markers',
                line=dict(width=1, color='red'),
                opacity=1
            )
        )

    fig.update_layout(
        showlegend=False,
        geo=dict(
            scope='north america',
            projection_type='azimuthal equal area',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        )
    )

    return fig
