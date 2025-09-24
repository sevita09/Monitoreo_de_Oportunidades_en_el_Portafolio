from dash import html, dcc, Input, Output, callback

@callback(
    Output('pagina_renta_variable', 'children'),
    Input('tabs', 'value'))
def pagina_renta_variable(tab):
  if tab == 'tab_renta_variable':
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
    ]);
  else:
    return html.Div();