from dash import html, dcc, Input, Output, callback

@callback(
    Output('pagina_renta_fija', 'children'),
    Input('tabs', 'value'))
def pagina_renta_fija(tab):
  if tab == 'tab_renta_fija':
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
      ]);
  else:
    return html.Div();