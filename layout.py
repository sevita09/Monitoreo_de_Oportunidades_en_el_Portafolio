import dash_bootstrap_components as dbc
from dash import Input, Output, html, callback
from paginas.pagina_datos_macro import pagina_datos_macro
from paginas.pagina_renta_fija import pagina_renta_fija
from paginas.pagina_renta_variable import pagina_renta_variable
from paginas.funciones_datos_macro.dolar_oficial import grafico_del_dolar

def create_sidebar():
    sidebar = html.Div([
        dbc.Nav(
            [
                dbc.NavLink([
                    html.I(className="fas fa-landmark me-2"), 
                    html.Span("Datos macro")],
                    href="/datos_macro",
                    active="exact",
                ),
                dbc.NavLink([
                        html.I(className="fas fa-chart-line me-2"),
                        html.Span("Renta variable"),
                    ],
                    href="/renta_variable",
                    active="exact",
                ),
                dbc.NavLink([
                        html.I(className="fas fa-money-check-alt me-2"),
                        html.Span("Renta fija"),
                    ],
                    href="/renta_fija",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True
        ),
    ],
    className="sidebar"
    )
    return sidebar

def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavLink(
                [html.I(className="fab fa-github-alt me-2")],
                href="https://github.com/sevita09/Monitoreo_de_Oportunidades_en_el_Portafolio",
                active="exact",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(html.I(id="dark_mode_sol", className="fas fa-sun modo_oscuro_claro_sol", style={"color":"white"})),
                    dbc.DropdownMenuItem(html.I(id="dark_mode_luna", className="fas fa-moon modo_oscuro_claro_luna", style={"color":"white"}))
                ],
                label=html.I(id="dark_mode", className="fa fa-adjust"),
                color="primary",
                nav=True,
                in_navbar=True,
            ),
        ],
        brand=[
            dbc.Container([
                html.Img(src="https://i.postimg.cc/kGMK8dCc/Captura-de-pantalla-2025-09-28-a-la-s-12-56-16-a-m.png", height="40px"),
                dbc.NavbarBrand("MOP", className="nav-brand-name")
            ])
        ],
        brand_href="/",
        color="dark",
        dark=True,
        sticky="top",
        fluid=True
    )
    return navbar

def create_content():
    return html.Div(
        id="page-content", 
        className="content"
    )

# Manejo del modo oscuro/claro
@callback(Output("dark_mode", "n_clicks"),
          Output("dark_mode_sol", "n_clicks"),
          Output("dark_mode_luna", "n_clicks"),
          Input("dark_mode_sol", "n_clicks"),
          Input("dark_mode_luna", "n_clicks"))
def dark_mode_class(n_clicks_sol, n_clicks_luna):
    if n_clicks_sol is None and n_clicks_luna is None:
        return 1, 2, 4  # Modo oscuro por defecto (1)
    if n_clicks_sol is None:
        n_clicks_sol = 2
    if n_clicks_luna is None:
        n_clicks_luna = 4
    if n_clicks_sol == 3:
        return 100, 2, 4  # Modo claro (2)
    elif n_clicks_luna == 5:
        return 1, 2, 4   # Modo oscuro (1)
    else:
        return 1, 2, 4   # Modo oscuro (1)
        

# Seteo el contenido de la página según la URL
@callback(Output("page-content", "children"), 
          Input("url", "pathname"),
          Input("dark_mode", "n_clicks"))
def render_page_content(pathname, dark_mode):
    if dark_mode is None:
        dark_mode_data = "bg-dark"  # Modo oscuro por defecto
    elif dark_mode >= 100:
        dark_mode_data = "bg-light"  # Modo claro
    else:
        dark_mode_data = "bg-dark"  # Modo oscuro

    if pathname == "/":
        return html.P("This is the home page!")
    elif pathname == "/datos_macro":
        return pagina_datos_macro(dark_mode_data)
    elif pathname == "/renta_variable":
        return pagina_renta_variable()
    elif pathname == "/renta_fija":
        return pagina_renta_fija()
    # Si la URL no coincide con ninguna de las anteriores, devuelvo un 404
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 rounded-3",
    )