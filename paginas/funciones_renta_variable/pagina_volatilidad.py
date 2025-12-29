from dash import html, Input, Output, callback
import numpy as np
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


@callback(
    [Output('grafico_de_volatilidad', 'figure'),
     Output('valor_actual_volatilidad', 'children'),
     Output('std_volatilidad', 'children'),
     Output('z_volatilidad', 'children'),
     Output('std_valor_volatilidad', 'children')],
    [Input('url', 'pathname'),
     Input('ticker_volatilidad', 'value'),
     Input('dias_volatilidad', 'value'),
     Input('bins_volatilidad', 'value'),
     Input('dark_mode', 'n_clicks')]
)
def grafico_de_volatilidad(path, ticker, dias, bins, dark_mode):
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
        if ticker is None or ticker == "":
            ticker = 'AAPL'

        # Descargar datos
        end = pd.Timestamp.today().normalize()
        start = end - pd.Timedelta(days=dias)
        try:
            data = yf.download(ticker, start=start, end=end + pd.Timedelta(days=1), progress=False, threads=False)
        except Exception:
            data = pd.DataFrame()

        if data.empty or 'Close' not in data.columns:
            # Devolver None para gráficos y vacíos para textos
            return None, "-", "-", "-", "-"

        close = data['Close']
        
        # EMA200
        ema200 = close.ewm(span=200, adjust=False).mean()
        print("EMA200 values list:", ema200.values.tolist())
        
        # Desviación porcentual respecto a EMA200
        deviation = ((close - ema200) / ema200) * 100
        deviation = deviation.dropna()
        deviation = np.array(deviation.values).flatten().tolist()
        print("deviation values list:", deviation)
        print(f"Ticker Name: {ticker}")
        mean_dev = np.mean(deviation)
        print(f"mean_dev: {mean_dev}")
        current_dev = deviation[-1] if deviation else 0
        print(f"current_dev: {current_dev}")
        std_dev = np.std(deviation)
        print(f"std_dev: {std_dev}")
        
        z = (current_dev - mean_dev) / std_dev if std_dev != 0 else 0
        
        print(f"z: {z}")

        print(f"Ticker: {ticker}, Current Dev: {current_dev}, Mean: {mean_dev}, Std: {std_dev}, Z: {z}")

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

        fig.update_layout(title_text=f'Histograma de desviación % respecto EMA200 - {ticker.upper()}',
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

        return fig, valor_actual_text, std_text, z_text, std_val_text
    else:
        return None, None, None, None, None
