from dash import html
from dash import dcc

def build_card(title=None, children=[], footer=[]):
    '''
    This function will return a html.Div object, with
    the correct formatting for a card. A title and children
    should be provided.
    '''
    card_children = []

    if title:
        card_children.append(
            html.Div(className='card-header', children=title)
        )

    card_children.append(
        html.Div(className='card-body', children=children)
    )

    if footer:
        card_children.append(
            html.Div(className='card-footer text-muted', children=footer)
        )

    return html.Div(className='card', children=card_children)

def build_notification(message='', type='primary'):
    className='alert alert-{}'.format(type)

    return html.Div(className=className, children=[
        html.Span(children=['Test'])
    ])