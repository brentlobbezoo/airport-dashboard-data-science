from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import overview, relations, classification

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Header(children=[
        html.Nav(className='navbar navbar-expand-lg navbar-light bg-light', children=[
            html.Div(className='container container-fluid', children=[
                html.Span(className='navbar-brand mb-0 h1', children='Assignment 4'),
                html.Div(className='', children=[
                    html.Div(className='navbar-nav', children=[
                        dcc.Link('Overview', className='nav-link', href='/'),
                        dcc.Link('Relations', className='nav-link', href='/relations'),
                        dcc.Link('Classification', className='nav-link', href='/classification')
                    ])
                ])
            ])
        ])
    ]),
    html.Main(children=[
        html.Div(id='page-content', className='container p-3')
    ]),
    html.Div(className='container', children=[
        html.Footer(className='d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top', children=[
            html.Div(className='col-12 d-flex flex-column align-items-center', children=[
                html.P(className='text-muted text-center', children=[
                    'Disclaimer: The dataset used is a reduced dataset. From the original dataset all the cancelled flights have been extracted. Then, from each month 10.000 random selected entries have been added to the dataset with cancelled flights. This resulted in a dataset with 120.633 rows.'
                ]),
                html.P(className='text-muted', children=[
                    '© Brent Lobbezoo (7791232), Stephan Berende (1727885) & Rachid Rahaui (6953905)'
                ])
            ])
        ])
    ])
])

@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def display_value(pathname):
    if pathname == '/':
        return overview.layout
    elif pathname == '/relations':
        return relations.layout
    elif pathname == '/classification':
        return classification.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)