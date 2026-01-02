from dash import html, Input, Output, callback, no_update
import numpy as np
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time


# Listas de ejemplo (puedes ajustar con tu universo real)
LISTA_LIDER = ['GGAL', 'PAMP', 'YPF', 'BMA']
LISTA_GENERAL = ['EDN', 'TRAN', 'CEPU', 'ALUA', 'BYMA']
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


@callback(
    Output('ticker_dropdown_suggestions', 'options'),
    Input('categoria_volatilidad', 'value')
)
def poblar_tickers_por_categoria(categoria):
    # Devuelve options para el dcc.Dropdown según categoría seleccionada
    if categoria == 'Lider':
        opts = [{'label': t, 'value': t} for t in LISTA_LIDER]
    elif categoria == 'General':
        opts = [{'label': t, 'value': t} for t in LISTA_GENERAL]
    else:
        opts = [{'label': t, 'value': t} for t in LISTA_CEDEAR]
    return opts


@callback(Output('ticker_volatilidad', 'value'), Input('ticker_dropdown_suggestions', 'value'))
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
     Output('std_valor_volatilidad', 'children'),
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
        # Valores de modo oscuro/claro coherentes con el proyecto
        if dark_mode is None:
            dark_mode_number = "#353a3f"
            dark_mode_font = "white"
        elif dark_mode >= 100:
            dark_mode_number = "#f9f9fa"
            dark_mode_font = "#054a7a"
        else:
            dark_mode_number = "#353a3f"
            dark_mode_font = "white"

        # Validaciones y valores por defecto
        try:
            dias = int(dias) if dias is not None else 500
        except Exception:
            dias = 500
        try:
            bins = int(bins) if bins is not None else 30
        except Exception:
            bins = 30

        # Determinar ticker a partir del input (es libre, puede venir de datalist o escrito)
        ticker = None
        if ticker_input is not None and str(ticker_input).strip() != "":
            ticker = str(ticker_input).strip()
        else:
            # valor por defecto según categoría
            if categoria == 'Cedear':
                ticker = 'AAPL'
            else:
                ticker = 'GGAL'

        # Si la categoría es Lider o General, asegurarse del sufijo .BA
        if categoria in ('Lider', 'General') and not ticker.upper().endswith('.BA'):
            ticker_download = f"{ticker}.BA"
        else:
            ticker_download = ticker

        descargar_series = descargar_serie(ticker_download, pd.Timestamp.today() - pd.Timedelta(days=dias*2), pd.Timestamp.today())
        data = descargar_series[0]
        err_msg = descargar_series[1]

        if data.empty or 'Close' not in data.columns:
            # Mostrar toast de error (se auto-cierra en 3s)
            msg = f"No se pudo descargar {ticker_download} tras 3 intentos."
            return None, "-", "-", "-", "-", True, msg

        # Serie de cierre base
        close = data['Close']

        print("en_dolares", en_dolares)
        # Si se pidió la conversión a dólares, dividir por (GGAL.BA * 10 / GGAL) por fecha
        if en_dolares:
            # Descargar series de GGAL.BA y GGAL
            ggal_ba, err_msg = descargar_serie('GGAL.BA', pd.Timestamp.today() - pd.Timedelta(days=dias*2), pd.Timestamp.today())
            ggal, err_msg = descargar_serie('GGAL', pd.Timestamp.today() - pd.Timedelta(days=dias*2), pd.Timestamp.today())
            if not ggal_ba.empty and not ggal.empty and 'Close' in ggal_ba.columns and 'Close' in ggal.columns:
                ggal_merged = pd.merge(ggal_ba['Close'], ggal['Close'], left_index=True, right_index=True, suffixes=('_BA', ''))
                ggal_merged.columns = ['Close_GGAL.BA', 'Close_GGAL']

                # Calcular el ratio
                ggal_merged['Ratio_GGAL.BA_GGAL'] = ggal_merged['Close_GGAL.BA'] / ggal_merged['Close_GGAL']
                
                
                # Extraer series de cierre y preparar denominador GGAL.BA*10 / GGAL
                ggal_ba_series = ggal_ba['Close'] * 10
                ggal_series = ggal['Close']
                # Asignar nombres para evitar errores al concatenar
                ggal_ba_series.name = 'GGAL.BA'
                ggal_series.name = 'GGAL'
                # Concatenar por índice (fechas) y quedarnos con la intersección
                denom_df = pd.concat([ggal_ba_series, ggal_series], axis=1, join='inner')
                if denom_df.empty:
                    msg = f"No hay datos coincidentes para GGAL.BA y GGAL para convertir a dólares."
                    return None, "-", "-", "-", "-", True, msg
                denom_series = denom_df['GGAL.BA'] / denom_df['GGAL']
                # Evitar divisiones por cero
                denom_series = denom_series.replace(0, np.nan)
                # Reindexar el denominador a las mismas fechas de la serie principal y rellenar
                denom_aligned = denom_series.reindex(data.index).ffill().bfill()
                print("denom_aligned", denom_aligned)
                print("close before", close)
                print("data_close", data['Close'])
                # Calcular la serie de precios en dólares
                close = data['Close'].divide(denom_aligned)
                print("close after2", close)
                # Si el resultado es todo NaN, informar error
                if close.dropna().empty:
                    msg = f"La conversión a dólares falló por falta de datos coincidentes."
                    return None, "-", "-", "-", "-", True, msg
            else:
                # Mostrar toast de error (se auto-cierra en 3s)
                msg = f"No se pudo descargar {ticker_download} tras 3 intentos."
                return None, "-", "-", "-", "-", True, msg

        # EMA200
        ema200 = close.ewm(span=200, adjust=False).mean()

        # Desviación porcentual respecto a EMA200
        deviation_series = ((close - ema200) / ema200) * 100
        deviation_series = deviation_series.dropna()
        deviation = deviation_series.values.flatten().tolist()
        mean_dev = float(np.mean(deviation)) if len(deviation) else 0.0
        current_dev = float(deviation[-1]) if len(deviation) else 0.0
        std_dev = float(np.std(deviation)) if len(deviation) else 0.0
        z = (current_dev - mean_dev) / std_dev if std_dev != 0 else 0.0

        # Histograma
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=deviation, nbinsx=bins, marker_color='rgba(100,150,255,0.8)', name='Distribución'))

        # Líneas: media, current, ±1σ, ±2σ
        fig.add_vline(x=current_dev, line=dict(color='red', width=2), annotation_text=f'Actual: {current_dev:.2f}%', annotation_position='top left')
        fig.add_vline(x=mean_dev, line=dict(color='yellow', width=1, dash='dash'), annotation_text=f'Media: {mean_dev:.2f}%', annotation_position='top right')
        if std_dev > 0:
            fig.add_vline(x=mean_dev + std_dev, line=dict(color='rgba(0,255,0,0.6)', width=1, dash='dot'), annotation_text=f'+1σ: {mean_dev+std_dev:.2f}%', annotation_position='top right')
            fig.add_vline(x=mean_dev - std_dev, line=dict(color='rgba(0,255,0,0.6)', width=1, dash='dot'))
            fig.add_vline(x=mean_dev + 2*std_dev, line=dict(color='rgba(0,180,0,0.4)', width=1, dash='dot'))
            fig.add_vline(x=mean_dev - 2*std_dev, line=dict(color='rgba(0,180,0,0.4)', width=1, dash='dot'))

        fig.update_layout(title_text=f'Histograma de desviación % respecto EMA200 - {ticker_download.upper()}',
                          xaxis_title='Desviación (%)',
                          yaxis_title='Frecuencia',
                          paper_bgcolor=dark_mode_number,
                          plot_bgcolor=dark_mode_number,
                          font_color=dark_mode_font,
                          margin={'t': 40, 'b': 20, 'l': 10, 'r': 10},
                          bargap=0.05)

        # Outputs de texto
        valor_actual_text = f"{current_dev:.2f}%"
        std_text = f"{std_dev:.4f}%"
        z_text = f"{z:.2f} σ"
        std_val_text = f"1σ = {std_dev:.4f}%"

        # No hay error: aseguramos toast cerrado
        return fig, valor_actual_text, std_text, z_text, std_val_text, False, ""
    else:
        return None, None, None, None, None, False, ""
