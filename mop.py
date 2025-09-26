from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from paginas.datos_pais import pagina_datos_del_pais
from paginas.pagina_renta_fija import pagina_renta_fija
from paginas.pagina_renta_variable import pagina_renta_variable

app = Dash(__name__,
           use_pages=True,
           pages_folder="paginas",
           assets_folder="assets",
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
           #external_stylesheets=[dbc.themes.COSMO, dbc.icons.FONT_AWESOME],
           )

# Quitar para probar en local y agregar para desplegar en Prod
#server = app.server

app.title = "MOP - Monitoreo de Oportunidades en el Portafolio"
app.config.suppress_callback_exceptions = True

sidebar = html.Div([
    dbc.Nav([
        dbc.NavLink([
           # html.I(className="fas fa-home me-2"),
            html.I(className="flag-icon-ar me flag-icon"), 
            html.Span("Datos del país")
            ],
            href="/datos_pais",
            active="exact",
        ),
        dbc.NavLink([
            html.I(className="fas fa-chart-simple me-2"),
            html.Span("Market"),
        ],
            href="/renta_fija",
            active="exact",
        ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Lado izquierdo: logo + nombre
            dbc.NavbarBrand(
                [
                    html.Img(src="https://via.placeholder.com/40", height="30px", className="me-2"),
                    "Mi Sitio"
                ],
                href="/",  # link a home
                className="d-flex align-items-center"
            ),

            # Lado derecho
            dbc.Nav(
                [
                    # Botón GitHub
                    dbc.NavItem(
                        dbc.NavLink("GitHub", href="https://github.com/", target="_blank")
                    ),

                    # Dropdown de temas
                    dbc.DropdownMenu(
                        [html.I(className="fa fa-sun me-2")],
                        children=[
                            dbc.DropdownMenuItem("Light", [html.I(className="fa fa-sun me-2")], id="theme-light"),
                            dbc.DropdownMenuItem("Dark", [html.I(className="fa fa-moon me-2")], id="theme-dark")
                        ],
                        nav=True,
                        in_navbar=True,
                        align_end=True,
                    ),
                ],
                className="ms-auto",  # alinea a la derecha
                navbar=True
            ),
        ]
    ),
    color="primary",
    dark=True,
)

app.layout = html.Div([
    navbar,
    html.Div([
        sidebar,
        page_container
    ],
    className="content")
])

if __name__ == '__main__':
    app.run(debug=False)