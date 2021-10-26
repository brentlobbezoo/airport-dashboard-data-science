from dash import html
from dash import dcc

def build_card(title=None, children=[], footer=[]):
    '''
    This function will return a html.Div object, with
    the correct formatting for a card. A title and children
    should be provided.
    '''
    body = []

    if title:
        body.append(
            html.H5(className='card-title', children=title)
        )

    body.extend(children)

    if footer:
        body.append(
            html.Div(className='card-footer text-muted', children=footer)
        )

    return html.Div(className='card', children=[
        html.Div(className='card-body', children=body)
    ])