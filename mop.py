from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

# Crear la app antes de importar módulos que registran callbacks
app = Dash(
    external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.FONT_AWESOME]
)
app.title = "MOP - Monitoreo de Oportunidades en el Portafolio"

# Habilitar registro de callbacks que referencian componentes que se cargan dinámicamente
app.config.suppress_callback_exceptions = True
app._favicon = ("../assets/icono.ico")

# Quitar para probar en local y agregar para desplegar en Prod
server = app.server

# Importar layout (y con ello las funciones de página) después de crear la app
from layout import create_navbar, create_sidebar, create_content

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