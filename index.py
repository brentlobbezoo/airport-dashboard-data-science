from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import overview, relations, lorem_ipsum

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
                        dcc.Link('Lorem ipsum', className='nav-link', href='/lorem-ipsum')
                    ])
                ])
            ])
        ])
    ]),
    html.Main(children=[
        html.Div(id='page-content', className='container p-3')
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
    elif pathname == '/lorem-ipsum':
        return lorem_ipsum.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)