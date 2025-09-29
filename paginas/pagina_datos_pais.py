from dash import html, dcc

def pagina_datos_del_pais():
  return html.Div([
    html.H3('Datos del país'),
    dcc.Graph(
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [1, 2, 3],
                'type': 'bar'
            }]
        }
    )
    ])
