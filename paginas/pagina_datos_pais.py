from dash import html, dcc, Input, Output, callback
from paginas.funciones_datos_pais.dolar_oficial import grafico_del_dolar
from paginas.funciones_datos_pais.pagina_dolar_oficial import pagina_datos_del_dolar_oficial

@callback(
    Output('pagina_datos_del_pais', 'children'),
    Input('tabs', 'value'))
def pagina_datos_del_pais(tab):
  if tab == 'tab_datos_pais':
    return html.Div(id="pagina_datos_del_dolar_oficial");
  else:
    return html.Div();