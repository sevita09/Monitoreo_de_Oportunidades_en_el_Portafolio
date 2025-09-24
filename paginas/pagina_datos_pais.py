from dash import html, dcc, Input, Output, callback
from paginas.funciones_datos_pais.dolar_oficial import grafico_del_dolar

@callback(
    Output('pagina_datos_del_pais', 'children'),
    Input('tabs', 'value'))
def pagina_datos_del_pais(tab):
  if tab == 'tab_datos_pais':
    return html.Div([
      html.H3('Datos del país'),
      dcc.Graph(id="grafico_del_dolar",
                figure=None),
      dcc.Graph(id="nivel_del_valor_del_dolar",
                figure=None),
      html.Div([
        html.Div([
          html.H2('Valor del dolar: '),
          html.H2(id="valor_del_dolar",
                  children=None)
        ],style={'justify-content': 'center'}),
        html.Div([
          html.H2('Valor de la banda superior: '),
          html.H2(id="banda_superior",
                  children=None)
        ],style={'justify-content': 'center'}),
        html.Div([
          html.H2('Valor de la banda inferior: '),
          html.H2(id="banda_inferior",
                  children=None)
        ],style={'justify-content': 'center'}),
        html.Div([
          html.H2('Variación de hoy: '),
          html.H2(id="variacion_del_dolar_d",
                  children=None)
        ],style={'justify-content': 'center'}),
        html.Div([
          html.H2('Variación del mes: '),
          html.H2(id="variacion_del_dolar_m",
                  children=None)
        ],style={'justify-content': 'center'}),
        html.Div([
          html.H2('Variación Y2D: '),
          html.H2(id="variacion_del_dolar_y2d",
                  children=None)
        ],style={'justify-content': 'center'})],
        style={'display': 'flex', 'justify-content': 'center'}
      )
    ]);
  else:
    return html.Div();