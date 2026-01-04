from dash import html, Input, Output, callback, no_update
import numpy as np
import requests
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
from lxml import html as html_parser


# Listas de ejemplo (puedes ajustar con tu universo real)
LISTA_LIDER = ['GGAL', 'PAMP', 'YPF', 'BMA']
LISTA_GENERAL = ['MORI', 'EDN', 'TRAN', 'CEPU', 'ALUA', 'BYMA']
LISTA_CEDEAR = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'NVDA']

# Descarga de serie desde yfinances de un ticker con 3 reintentos o cartel de error
def descargar_serie(ticker, start, end, max_reintentos=3):
    data = pd.DataFrame()
    last_err_msg = ''
    for attempt in range(max_reintentos):
        try:
            data = yf.download(ticker, start=start, end=end + pd.Timedelta(days=1), progress=False, threads=False, multi_level_index=False)
            if not data.empty and 'Close' in data.columns:
                break
        except Exception as e:
            last_err_msg = str(e)
        time.sleep(0.5)
    data = data.dropna()
    return data, last_err_msg

def obtener_logo(ticker, categoria):
    # Encabezados para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9"
    }

    url_ticker = f"https://es.tradingview.com/symbols/{ticker}/" if categoria == 'Cedear' else f"https://es.tradingview.com/symbols/BCBA-{ticker[:-3]}/"
    url = "https://i.postimg.cc/kGMK8dCc/Captura-de-pantalla-2025-09-28-a-la-s-12-56-16-a-m.png"
    try:
        response = requests.get(url_ticker, headers=headers, timeout=10)
        response.raise_for_status()

        tree = html_parser.fromstring(response.content)

        # XPath Flexible que busca la URL completa del logo
        xpath_query = '//img[contains(@src, "s3-symbol-logo.tradingview.com")]/@src'
        
        urls_encontradas = tree.xpath(xpath_query)

        if urls_encontradas:
            # Devuelve la primera URL encontrada directamente
            return urls_encontradas[0]
        else:
            return url # Retorna la imagen del site

    except Exception:
        return url

def get_dark_mode_colors(dark_mode):
    """Return background color and font color depending on dark_mode value."""
    if dark_mode is None:
        return "#353a3f", "white"
    if dark_mode >= 100:
        return "#f9f9fa", "#54a2e1"
    return "#353a3f", "white"
    
def sanitize_inputs(categoria, ticker_input, dias, bins):
    """Normalize inputs and return (ticker_download, dias, bins)."""
    try:
        dias = int(dias) if dias is not None else 500
    except Exception:
        dias = 500
    try:
        bins = int(bins) if bins is not None else 30
    except Exception:
        bins = 30

    if ticker_input is not None and str(ticker_input).strip() != "":
        ticker = str(ticker_input).strip()
    else:
        if categoria == 'Lider':
            ticker = 'GGAL'
        elif categoria == 'General':
            ticker = 'MORI'
        else:
            ticker = 'AAPL'

    if categoria in ('Lider', 'General') and not ticker.upper().endswith('.BA'):
        ticker_download = f"{ticker}.BA"
    else:
        ticker_download = ticker

    return ticker_download, dias, bins


def _prepare_denom_series(ggal_ba_df, ggal_df, target_index):
    """Given dataframes for GGAL.BA and GGAL, return an aligned denom Series (GGAL.BA*10 / GGAL) reindexed to target_index.

    Raises ValueError if there are no overlapping dates.
    """
    ggal_ba_series = ggal_ba_df['Close'] * 10
    ggal_series = ggal_df['Close']
    ggal_ba_series.name = 'GGAL.BA'
    ggal_series.name = 'GGAL'
    denom_df = pd.concat([ggal_ba_series, ggal_series], axis=1, join='inner')
    if denom_df.empty:
        raise ValueError("No overlapping dates for GGAL.BA and GGAL")
    denom_series = denom_df['GGAL.BA'] / denom_df['GGAL']
    denom_series = denom_series.replace(0, np.nan)
    denom_aligned = denom_series.reindex(target_index).ffill().bfill()
    return denom_aligned


def compute_deviation_stats(close, ema200):
    """Compute EMA200, deviation series and basic stats from a close Series. Returns (deviation_list, mean, current, std)."""
    # Desviación porcentual respecto a EMA200
    deviation_series = ((close - ema200) / ema200) * 100
    deviation_series = deviation_series.dropna()
    deviation = deviation_series.values.flatten().tolist()
    mean_dev = float(np.mean(deviation)) if len(deviation) else 0.0
    current_dev = float(deviation[-1]) if len(deviation) else 0.0
    std_dev = float(np.std(deviation)) if len(deviation) else 0.0
    z = (current_dev - mean_dev) / std_dev if std_dev != 0 else 0.0
    return deviation, mean_dev, current_dev, std_dev, z


def construir_histograma(deviation, bins, dark_mode_number, dark_mode_font, current_dev, mean_dev, std_dev, ticker_download, en_dolares, categoria):
    # Histograma
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=deviation, nbinsx=bins, marker_color='rgba(100,150,255,0.8)', name='Distribución'))

    # Líneas: media, current, ±1σ, ±2σ
    fig.add_vline(x=current_dev, line=dict(color='red', width=2), annotation_text=f'Actual: {current_dev:.2f}%', annotation_position='top right')
    fig.add_vline(x=mean_dev, line=dict(color='yellow', width=1, dash='dash'), annotation_text=f'Media: {mean_dev:.2f}%', annotation_position='top right')
    if std_dev > 0:
        fig.add_vline(x=mean_dev + std_dev, line=dict(color='rgba(0,255,0,0.6)', width=1, dash='dot'), annotation_text=f'+σ: {mean_dev+std_dev:.2f}%', annotation_position='bottom right')
        fig.add_vline(x=mean_dev - std_dev, line=dict(color='rgba(0,255,0,0.6)', width=1, dash='dot'), annotation_text=f'-σ: {mean_dev-std_dev:.2f}%', annotation_position='bottom right')
        fig.add_vline(x=mean_dev + 2*std_dev, line=dict(color='rgba(0,180,0,0.4)', width=1, dash='dot'), annotation_text=f'+2σ: {mean_dev+2*std_dev:.2f}%', annotation_position='bottom right')
        fig.add_vline(x=mean_dev - 2*std_dev, line=dict(color='rgba(0,180,0,0.4)', width=1, dash='dot'), annotation_text=f'-2σ: {mean_dev-2*std_dev:.2f}%', annotation_position='bottom right')

    dolar = 'en Dolares' if en_dolares or categoria == 'Cedear' else 'en Pesos'

    fig.update_layout(title_text=f'Histograma de desviación % respecto EMA200 - {ticker_download.upper()} {dolar}',
                        xaxis_title='Desviación (%)',
                        yaxis_title='Frecuencia',
                        paper_bgcolor=dark_mode_number,
                        plot_bgcolor=dark_mode_number,
                        font_color=dark_mode_font,
                        margin={'t': 40, 'b': 20, 'l': 10, 'r': 10},
                        bargap=0.05)

    return fig


@callback(
    [Output('ticker_dropdown_suggestions', 'options'),
    Output('ticker_dropdown_suggestions', 'value'),
    Output('ticker_dropdown_suggestions', 'disabled'),
    Output('dolares_volatilidad', 'disabled')],
    Input('categoria_volatilidad', 'value')
)
def poblar_tickers_por_categoria(categoria):
    # Devuelve options para el dcc.Dropdown según categoría seleccionada
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


@callback(Output('ticker_volatilidad', 'value'), 
          Input('ticker_dropdown_suggestions', 'value'))
def copiar_sugerencia_en_input(sugerencia):
    # Cuando se selecciona una sugerencia, la copiamos automáticamente al input
    if sugerencia is None:
        return no_update
    return sugerencia


@callback(
    [Output('grafico_de_volatilidad', 'figure'),
     Output('valor_actual_volatilidad', 'children'),
     Output('std_volatilidad', 'children'),
     Output('z_volatilidad', 'children'),
     Output('valor_media', 'children'),
     Output('valor_menos_dos_sigma', 'children'),
     Output('valor_menos_sigma', 'children'),
     Output('valor_sigma', 'children'),
     Output('valor_dos_sigma', 'children'),
     Output('dolares_volatilidad', 'on'),
     Output('logo_url', 'src'),
     Output('toast_error', 'is_open'),
     Output('toast_error', 'children')],
    [Input('url', 'pathname'),
     Input('categoria_volatilidad', 'value'),
     Input('ticker_volatilidad', 'value'),
     Input('dias_volatilidad', 'value'),
     Input('bins_volatilidad', 'value'),
     Input('dolares_volatilidad', 'on'),
     Input('dark_mode', 'n_clicks')]
)
def grafico_de_volatilidad(path, categoria, ticker_input, dias, bins, en_dolares, dark_mode):
    if path == '/renta_variable/volatilidad':
        # Colors
        dark_mode_number, dark_mode_font = get_dark_mode_colors(dark_mode)

        # Sanitize inputs and get ticker to download
        ticker_download, dias, bins = sanitize_inputs(categoria, ticker_input, dias, bins)

        # Download main series
        data, err_msg = descargar_serie(ticker_download, pd.Timestamp.today() - pd.Timedelta(days=dias*2), pd.Timestamp.today())
        
        if categoria == 'Cedear':
            en_dolares = True

        logo_url = obtener_logo(ticker_download, categoria)

        if data.empty or 'Close' not in data.columns:
            msg = f"No se pudo descargar {ticker_download} tras 3 intentos."
            return None, "-", "-", "-", "-", "-", "-", "-", "-", en_dolares, logo_url, True, msg

        # Base close series
        close = data['Close']

        # If requested, convert to dollars using GGAL reference
        if en_dolares and categoria != 'Cedear':
            try:
                ggal_ba, _ = descargar_serie('GGAL.BA', pd.Timestamp.today() - pd.Timedelta(days=dias*2), pd.Timestamp.today())
                ggal, _ = descargar_serie('GGAL', pd.Timestamp.today() - pd.Timedelta(days=dias*2), pd.Timestamp.today())
                denom_aligned = _prepare_denom_series(ggal_ba, ggal, data.index)
                # ensure close is a Series
                close_series = data['Close']
                if isinstance(close_series, pd.DataFrame):
                    close_series = close_series.iloc[:, 0]
                close = close_series.reindex(denom_aligned.index).div(denom_aligned)
                if close.dropna().empty:
                    msg = f"La conversión a dólares falló por falta de datos coincidentes."
                    return None, "-", "-", "-", "-", "-", "-", "-", "-", en_dolares, logo_url, True, msg
            except Exception:
                msg = f"No se pudo descargar {ticker_download} tras 3 intentos."
                return None, "-", "-", "-", "-", "-", "-", "-", "-", en_dolares, logo_url, True, msg

        # EMA200
        ema200 = close.ewm(span=200, adjust=False).mean()

        # Desviación porcentual respecto a EMA200
        deviation, mean_dev, current_dev, std_dev, z = compute_deviation_stats(close, ema200)

        # Construir histograma
        fig = construir_histograma(deviation, bins, dark_mode_number, dark_mode_font, current_dev, mean_dev, std_dev, ticker_download, en_dolares, categoria)

        # Outputs de texto
        valor_actual_text = f"{current_dev:.2f}%"
        std_text = f"{std_dev:.2f}%"
        z_text = f"{z:.2f} σ"
        media_text = f"{mean_dev:.2f}%"
        menos_sigma_text = f"{(mean_dev - std_dev):.2f}%"
        menos_dos_sigma_text = f"{(mean_dev - 2*std_dev):.2f}%"
        sigma_text = f"{(mean_dev + std_dev):.2f}%"
        dos_sigma_text = f"{(mean_dev + 2*std_dev):.2f}%"

        # No hay error: aseguramos toast cerrado
        return fig, valor_actual_text, std_text, z_text, media_text, menos_dos_sigma_text, menos_sigma_text, sigma_text, dos_sigma_text, en_dolares, logo_url, False, ""
    else:
        return None, None, None, None, None, None, None, None, None, None, None, False, ""
