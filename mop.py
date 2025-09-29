from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from layout import create_navbar, create_sidebar, create_content
import dash_bootstrap_components as dbc

app = Dash(
    external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.FONT_AWESOME]
)
app.title = "MOP - Monitoreo de Oportunidades en el Portafolio"
app.config.suppress_callback_exceptions = True

# Quitar para probar en local y agregar para desplegar en Prod
server = app.server

navbar = create_navbar()
sidebar = create_sidebar()
content = create_content()

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,   
        sidebar,
        content
    ]
)



#app.layout = dbc.Container([
#    navbar,
#    dcc.Tabs(
#        id="tabs",
#        value='tab_datos_pais',
#        children=[
#          dcc.Tab(
#              label='Datos del país',
#              value='tab_datos_pais'),
#          dcc.Tab(
#              label='Renta Fija',
#              value='tab_renta_fija'),
#          dcc.Tab(
#              label='Renta Variable',
#              value='tab_renta_variable')
#    ],style={'display': 'flex', 'justify-content': 'center'}),
#    html.Div(id='pagina_datos_del_pais'),
#    html.Div(id='pagina_renta_fija'),
#    html.Div(id='pagina_renta_variable')
#], fluid=True,
#class_name='px-0')

if __name__ == '__main__':
    app.run(debug=True)