from dash import html, dcc

def pagina_renta_fija():
  return html.Div([
    html.H3('Renta Fija'),
    dcc.Graph(
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [3, 1, 2],
                'type': 'bar'
            }]
        }
    )
    ])