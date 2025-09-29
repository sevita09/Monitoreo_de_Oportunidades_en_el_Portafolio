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
#server = app.server

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

if __name__ == '__main__':
    app.run(debug=True)