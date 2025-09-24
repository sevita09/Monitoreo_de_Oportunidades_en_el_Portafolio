from dash import html, dcc, Input, Output, callback

@callback(
    Output('pagina_datos_del_pais', 'children'),
    Input('tabs', 'value'))
def pagina_datos_del_pais(tab):
  if tab == 'tab_datos_pais':
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
    ]);
  else:
    return html.Div();