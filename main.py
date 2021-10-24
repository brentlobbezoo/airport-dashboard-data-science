import dash
import plotly.express as px
import pandas as pd
import os

from datetime import date
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from card_builder import build_card

app = dash.Dash(__name__)
df = pd.read_csv(os.path.join(os.getcwd(), 'data.csv'))

@app.callback(
    Output(component_id='flights-per-month', component_property='figure'),
    Input(component_id='months', component_property='value')
)
def flights_per_month(months=None):
    df_copy = df.copy()

    if months:
        flights = df_copy[df_copy.Month.isin(months)]['Month'].value_counts().reset_index()
    else:
        flights = df_copy['Month'].value_counts().reset_index()

    return px.bar(flights, x='index', y='Month')

app.layout = html.Div(className='container p-3', children=[
    html.Div(className='row', children=[
        html.Div(className='col-3', children=[
            build_card(title='Filters', children=[
                html.Form(className='form', children=[
                    html.Div(className='mb-3', children=[
                        html.Label(className='form-label', children=[
                            'Months'
                        ]),
                        dcc.Dropdown(
                            id='months',
                            options=[
                                {
                                    'label': 'January',
                                    'value': 1
                                },
                                {
                                    'label': 'February',
                                    'value': 2
                                },
                                {
                                    'label': 'March',
                                    'value': 3
                                },
                                {
                                    'label': 'April',
                                    'value': 4
                                },
                                {
                                    'label': 'May',
                                    'value': 5
                                },
                                {
                                    'label': 'June',
                                    'value': 6
                                }
                            ],
                            multi=True,
                            className="dcc_control"
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
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)