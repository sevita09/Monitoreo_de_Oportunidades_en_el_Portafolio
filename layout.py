import dash_bootstrap_components as dbc
from dash import Input, Output, html, callback
from paginas.datos_pais import pagina_datos_del_pais
from paginas.pagina_renta_fija import pagina_renta_fija
from paginas.pagina_renta_variable import pagina_renta_variable

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
                    dbc.DropdownMenuItem(html.I(className="fas fa-sun modo_oscuro_claro_sol", style={"color":"white"})),
                    dbc.DropdownMenuItem(html.I(className="fas fa-moon modo_oscuro_claro_luna", style={"color":"white"}))
                ],
                label=html.I(className="fa fa-adjust"),
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

# set the content according to the current pathname
@callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the home page!")
    elif pathname == "/datos_macro":
        return pagina_datos_del_pais()
    elif pathname == "/renta_variable":
        return pagina_renta_variable()
    elif pathname == "/renta_fija":
        return pagina_renta_fija()
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )