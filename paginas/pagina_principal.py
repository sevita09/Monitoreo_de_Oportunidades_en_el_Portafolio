from dash import html

def pagina_principal(dark_mode):
    return html.Div(
        [
            html.Img(src="https://i.postimg.cc/kGMK8dCc/Captura-de-pantalla-2025-09-28-a-la-s-12-56-16-a-m.png")
        ],
        style={
            "display": "flex",          # Activa el modelo de caja flexible
            "justifyContent": "center", # Centrado horizontal
            "alignItems": "center",     # Centrado vertical
            "height": "100vh"           # Ocupa toda la altura de la ventana
        },
        className=dark_mode
    )