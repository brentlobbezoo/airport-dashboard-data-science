from dash import html

def build_card(title=None, children=[]):
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

    return html.Div(className='card', children=[
        html.Div(className='card-body', children=body)
    ])
