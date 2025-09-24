from dash import Dash, html, dcc
from paginas.datos_pais import pagina_datos_del_pais
from paginas.pagina_renta_fija import pagina_renta_fija
from paginas.pagina_renta_variable import pagina_renta_variable

app = Dash(__name__)

# Quitar para probar en local y agregar para desplegar en Prod
server = app.server

app.layout = html.Div([
    dcc.Tabs(
        id="tabs",
        value='tab_datos_pais',
        children=[
          dcc.Tab(
              label='Datos del país',
              value='tab_datos_pais'),
          dcc.Tab(
              label='Renta Fija',
              value='tab_renta_fija'),
          dcc.Tab(
              label='Renta Variable',
              value='tab_renta_variable')
    ],style={'display': 'flex', 'justify-content': 'center'}),
    html.Div(id='pagina_datos_del_pais'),
    html.Div(id='pagina_renta_fija'),
    html.Div(id='pagina_renta_variable')
])

if __name__ == '__main__':
    app.run(debug=False)