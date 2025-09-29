from dash import html, dcc

def pagina_renta_variable():
    return html.Div([
      html.H3('Renta Variable'),
      dcc.Graph(
          figure={
              'data': [{
                  'x': [1, 2, 3],
                  'y': [2, 3, 1],
                  'type': 'bar'
              }]
          }
      )
    ])