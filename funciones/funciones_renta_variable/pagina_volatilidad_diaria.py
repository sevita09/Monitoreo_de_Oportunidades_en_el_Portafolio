from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Importaciones estáticas (canonical)
from funciones.funciones_generales.obtener_datos import descargar_serie, dolarizar_serie_mep
from funciones.funciones_renta_variable.pagina_volatilidad import obtener_logo, LISTA_LIDER, LISTA_GENERAL, LISTA_CEDEAR


def colores_por_modo(dark_mode):
    """Devuelve colores de fondo y fuente según dark_mode."""
    if dark_mode is None:
        return "#353a3f", "white"
    if dark_mode >= 100:
        return "#f9f9fa", "#054a7a"
    return "#353a3f", "white"


def calcular_variacion_por_ventana(close, ventana_dias):

    retornos = (close.pct_change(periods=ventana_dias).dropna() * 100).tolist()

    media = float(np.mean(retornos)) if len(retornos) else 0.0
    actual = float(retornos[-1]) if len(retornos) else 0.0
    std = float(np.std(retornos)) if len(retornos) else 0.0
    return retornos, media, actual, std


def construir_histograma_span(deviation, bins, titulo, dark_bg, dark_font, actual, media, std):
    """Construye el histograma sin la caja de estadísticas interna."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=deviation, nbinsx=bins, marker_color='rgba(100,150,255,0.8)', name='Distribución'))

    # Líneas de referencia
    fig.add_vline(x=actual, line=dict(color='red', width=2))
    fig.add_vline(x=media, line=dict(color='yellow', width=1, dash='dash'))
    if std > 0:
        fig.add_vline(x=media + std, line=dict(color='rgba(0,255,0,0.6)', width=1, dash='dot'))
        fig.add_vline(x=media - std, line=dict(color='rgba(0,255,0,0.6)', width=1, dash='dot'))

    fig.update_layout(
        yaxis_title='Frecuencia',
        paper_bgcolor=dark_bg,
        plot_bgcolor=dark_bg,
        font_color=dark_font,
        margin={'t': 0, 'b': 20, 'l': 10, 'r': 10},
        bargap=0.05
    )
    return fig


@callback(
    [Output('graf_diaria_1_volatilidad_diaria', 'figure'), Output('graf_diaria_2_volatilidad_diaria', 'figure'), Output('graf_diaria_3_volatilidad_diaria', 'figure'),
     Output('graf_diaria_4_volatilidad_diaria', 'figure'), Output('graf_diaria_5_volatilidad_diaria', 'figure'), Output('graf_diaria_6_volatilidad_diaria', 'figure'),
     Output('titulo_diaria_1_volatilidad_diaria', 'children'), Output('titulo_diaria_2_volatilidad_diaria', 'children'), Output('titulo_diaria_3_volatilidad_diaria', 'children'),
     Output('titulo_diaria_4_volatilidad_diaria', 'children'), Output('titulo_diaria_5_volatilidad_diaria', 'children'), Output('titulo_diaria_6_volatilidad_diaria', 'children'),
     Output('stats_diaria_1_volatilidad_diaria', 'children'), Output('stats_diaria_2_volatilidad_diaria', 'children'), Output('stats_diaria_3_volatilidad_diaria', 'children'),
     Output('stats_diaria_4_volatilidad_diaria', 'children'), Output('stats_diaria_5_volatilidad_diaria', 'children'), Output('stats_diaria_6_volatilidad_diaria', 'children'),
     Output('logo_url_pagina_volatilidad_diaria', 'src'), Output('toast_error_pagina_volatilidad_diaria', 'is_open'), Output('toast_error_pagina_volatilidad_diaria', 'children')
    ],
    [Input('url', 'pathname'),
     Input('categoria_volatilidad_diaria', 'value'),
     Input('ticker_volatilidad_diaria', 'value'),
     Input('dias_volatilidad_diaria', 'value'),
     Input('bins_volatilidad_diaria', 'value'),
     Input('dolares_volatilidad_diaria', 'on'),
     Input('dark_mode', 'n_clicks')]
)
def actualizar_histogramas_pagina_volatilidad_diaria(path, categoria, ticker_input, dias, bins, dolares_on, dark_mode):
    # Solo actualizar cuando estemos en la ruta correspondiente
    if path != '/renta_variable/volatilidad_diaria':
        # Debemos devolver la misma cantidad de outputs: 6 figuras + 6 títulos + 6 stats
        return [None] * 6 + [None] * 6 + [None] * 6 + [None, False, ""]

    # Usamos importación estática de 'descargar_serie' y 'obtener_logo'

    dark_bg, dark_font = colores_por_modo(dark_mode)

    # Normalizar inputs
    try:
        dias = int(dias) if dias is not None else 500
    except Exception:
        dias = 500
    try:
        bins = int(bins) if bins is not None else 30
    except Exception:
        bins = 30

    ticker = (ticker_input or 'AAPL').strip()

    # Determinar ticker que se usará para descargar y obtener logo
    ticker_download = ticker if categoria == 'Cedear' else (ticker + '.BA' if not ticker.upper().endswith('.BA') else ticker)

    # Obtener logo usando la función importada estáticamente
    logo_url = ""
    try:
        logo_url = obtener_logo(ticker_download, categoria)
    except Exception:
        logo_url = ""

    # Preparar rango de fechas
    start = pd.Timestamp.today() - pd.Timedelta(days=dias*2)
    end = pd.Timestamp.today()

    # Si el usuario solicitó ver en dólares y no es un Cedear, intentamos dolarizar vía MEP
    if dolares_on and categoria != 'Cedear':
        data, msg = dolarizar_serie_mep(ticker_download, start, end, max_reintentos=3)
    else:
        data, msg = descargar_serie(
            ticker_download,
            start,
            end
        )

    if data is None or (hasattr(data, 'empty') and data.empty):
        empty_fig = go.Figure()
        empty_fig.update_layout(title_text='No hay datos')
        msg = f"No se pudo descargar {ticker_download} tras varios intentos."
        return [empty_fig] * 6 + [None] * 6 + [None] * 6 + [logo_url, True, msg]

    # Normalizar 'close' si el DataFrame viene con columna Close
    try:
        close = data['Close']
    except Exception:
        close = data

    # Ventanas en dias (aprox en días de trading)
    ventanas = [1, 2, 4, 9, 19, 59]
    titulos = ['Diaria', '3 días', 'Semanal', '15 días', 'Mensual', 'Trimestral']

    figuras = []
    titulos_out = []
    stats_out = []

    for v, titulo in zip(ventanas, titulos):
        deviation, media, actual, std = calcular_variacion_por_ventana(close, v)

        # Construir figura SIN el recuadro de estadísticas (ahora externo)
        fig = construir_histograma_span(deviation, bins, None, dark_bg, dark_font, actual, media, std)
        figuras.append(fig)

        # Título que irá encima del gráfico
        titulos_out.append(f"{titulo} - {ticker.upper()}")

        # Caja de estadísticas exterior (HTML)
        if std and std > 0:
            sigma_count = (actual - media) / std
            sigma_text = f"{sigma_count:.2f}σ"
        else:
            sigma_text = "N/A"

        stats_html = html.Div([
            html.Div([html.B('Actual: '), f"{actual:.2f}%",
            html.B('  Media: '), f"{media:.2f}%"]),
            html.Div([html.B('σ: '), f"{std:.2f}%",
            html.B('  Actual vs μ: '), sigma_text])
        ], style={'textAlign': 'center', 'width': '100%'})

        stats_out.append(stats_html)

    # Devolver: 6 figuras, 6 títulos, 6 stats, logo y toast cerrado
    return figuras + titulos_out + stats_out + [logo_url, False, ""]


# Compatibilidad de nombres: algunos módulos/layouts importan versiones
# con nombres diferentes. Exponer alias cortos/largos para evitar ImportError
try:
    # alias corto -> largo
    actualizar_histogramas = actualizar_histogramas_pagina_volatilidad_diaria
except NameError:
    # si por alguna razón el nombre largo no existe, no rompemos la importación
    pass


# Callbacks auxiliares: poblar sugerencias y copiar sugerencia al input (versión diaria)
@callback(
    [Output('ticker_dropdown_suggestions_volatilidad_diaria', 'options'),
     Output('ticker_dropdown_suggestions_volatilidad_diaria', 'value'),
     Output('ticker_dropdown_suggestions_volatilidad_diaria', 'disabled'),
     Output('dolares_volatilidad_diaria', 'disabled')],
    Input('categoria_volatilidad_diaria', 'value')
)
def poblar_tickers_por_categoria_volatilidad_diaria(categoria):
    if categoria == 'Lider':
        opts = [{'label': t, 'value': t} for t in LISTA_LIDER]
        ticker = 'GGAL'
        dolares_volatilidad = False
        ticker_dropdown_disabled = False
    elif categoria == 'General':
        opts = [{'label': t, 'value': t} for t in LISTA_GENERAL]
        ticker = 'MORI'
        dolares_volatilidad = False
        ticker_dropdown_disabled = False
    elif categoria == 'Cedear':
        opts = [{'label': t, 'value': t} for t in LISTA_CEDEAR]
        ticker = 'AAPL'
        dolares_volatilidad = True
        ticker_dropdown_disabled = False
    else:
        opts = []
        ticker = ''
        dolares_volatilidad = False
        ticker_dropdown_disabled = True

    return opts, ticker, ticker_dropdown_disabled, dolares_volatilidad


@callback(Output('ticker_volatilidad_diaria', 'value'),
          Input('ticker_dropdown_suggestions_volatilidad_diaria', 'value'))
def copiar_sugerencia_en_input_volatilidad_diaria(sugerencia):
    if sugerencia is None:
        return None
    return sugerencia

