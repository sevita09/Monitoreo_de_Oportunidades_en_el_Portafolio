from datetime import datetime, timedelta
from datetime import date
from dash import Input, Output, callback
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

from funciones.funciones_generales.obtener_datos import descargar_serie

def grafico_de_velas_dolar_mep_ccl(mep_ccl, data_dolar, dolar_EMA21, dolar_EMA100, dark_mode_number, dark_mode_font):
    title_text = "Dolar MEP" if mep_ccl == "mep" else "Dolar CCL"

    # Descargar datos del Dólar desde Yahoo Finance
    figCandles = go.Figure(data=[go.Candlestick(x=data_dolar.index,
                                        open=data_dolar.Open,
                                        high=data_dolar.High,
                                        low=data_dolar.Low,
                                        close=data_dolar.Close,
                                        increasing=dict(line=dict(color="#00BC00", width=3)), # Vela verde para subir
                                        decreasing=dict(line=dict(color="#BC0000", width=3)), # Vela roja para bajar
                                        opacity=1,
                                        name=title_text
                                        )],
                                        layout=go.Layout(
                                          title={'text': title_text, "y":0.97, "x":0.5, "xanchor": "center", "yanchor": "top"},
                                          margin={"t": 40, "b": 10, "l": 10, "r": 10},
                                          height=500,
                                          paper_bgcolor=dark_mode_number, 
                                          plot_bgcolor=dark_mode_number, 
                                          font_color=dark_mode_font
                                        ))
    figCandles.add_trace(go.Scatter(x=data_dolar.index, y=dolar_EMA21, mode='lines', name='EMA 21', line=dict(color='orange', width=1)))
    figCandles.add_trace(go.Scatter(x=data_dolar.index, y=dolar_EMA100, mode='lines', name='EMA 100', line=dict(color='purple', width=1)))
    figCandles.update_layout(xaxis_rangeslider_visible=False, paper_bgcolor=dark_mode_number, plot_bgcolor="black", font_color=dark_mode_font)
    figCandles.update_layout(
        xaxis_gridcolor='rgba(255,255,255,0.4)',  # Líneas de la cuadrícula en negro con 20% de opacidad
        yaxis_gridcolor='rgba(255,255,255,0.4)'   # Líneas de la cuadrícula en negro con 20% de opacidad
    )

    return figCandles

def calcular_dolar_mep(dia_inicial):
    # Calcula el dólar MEP dividiendo el valor del bono AL30 en pesos por su valor en dólares.

    ggal_ars, msg = descargar_serie("GGAL.BA", dia_inicial, datetime.today(), 3)
    if msg is not None:
        return None, msg
    
    ggald_usd, msg = descargar_serie("GGALD.BA", dia_inicial, datetime.today(), 3)
    if msg is not None:
        return None, msg
    
    return ggal_ars / ggald_usd, None

def calcular_dolar_ccl(dia_inicial):
    # Calcula el Contado con Liquidación (CCL) usando la relación entre GGAL en la bolsa local y su ADR.

    ggal_ars, msg = descargar_serie("GGAL.BA", dia_inicial, datetime.today(), 3)
    if msg is not None:
        return None, msg

    ggal_usd, msg = descargar_serie("GGAL", dia_inicial, datetime.today(), 3)
    if msg is not None:
        return None, msg

    # La fórmula es (GGAL:BCBA * 10) / GGAL:NYSE, ya que 1 ADR son 10 acciones locales.
    return (ggal_ars * 10) / ggal_usd, None

def primer_dia_habil_anual():
    # año actual
    año_actual = int(datetime.today().year)

    # Obtener el primer día del año
    fecha_inicial = date(año_actual, 1, 1)
    
    # Determinar el día de la semana (0=Lunes, 6=Domingo)
    dia_semana = fecha_inicial.weekday()
    
    if dia_semana == 5:  # Sábado
        dias_a_sumar = 2
    elif dia_semana == 6: # Domingo
        dias_a_sumar = 1
    else:
        dias_a_sumar = 0
        
    # Calcular la fecha del primer día hábil sumando los días
    primer_dia_habil = fecha_inicial + timedelta(days=dias_a_sumar)

    return primer_dia_habil.strftime("%Y-%m-%d")

def calcular_brechas_dolar(dia_inicial):
    # Calcula las brechas entre los distintos tipos de cambio y retorna un diccionario.

    dolar_oficial, msg = descargar_serie("USDARS=X", dia_inicial, datetime.today(), 3)
    if msg is not None:
        return None, msg
    dolar_mep, msg = calcular_dolar_mep(dia_inicial)
    if msg is not None:
        return None, msg
    
    dolar_ccl, msg = calcular_dolar_ccl(dia_inicial)
    if msg is not None:
        return None, msg

    brechas = {
        "oficial": dolar_oficial,
        "mep": dolar_mep,
        "ccl": dolar_ccl,
        "brecha_oficial_mep": None,
        "brecha_mep_ccl": None,
        "brecha_oficial_ccl": None
    }
    
    brechas["brecha_oficial_mep"] = ((dolar_mep / dolar_oficial) - 1) * 100
    brechas["brecha_mep_ccl"] = ((dolar_ccl / dolar_mep) - 1) * 100
    brechas["brecha_oficial_ccl"] = ((dolar_ccl / dolar_oficial) - 1) * 100
    return brechas, None

def valores_dolar_mep_ccl(data_dolar, dia_de_hoy, valor_dolar_primer_dia_del_ano):
    dia_de_hoy = -(dia_de_hoy+1)
    valor_del_dolar = data_dolar.Close.iloc[-1]
    dolar_EMA21 = data_dolar.Close.ewm(span=21, adjust=False).mean()
    dolar_EMA100 = data_dolar.Close.ewm(span=100, adjust=False).mean()
    media_movil_21 = data_dolar.Close.ewm(span=21, adjust=False).mean().iloc[-1]
    media_movil_100 = data_dolar.Close.ewm(span=100, adjust=False).mean().iloc[-1]
    emas = {
        'dolar_EMA21': dolar_EMA21,
        'dolar_EMA100': dolar_EMA100
    }
    valores_dolar = {'valor_del_dolar': round(valor_del_dolar,2).item(),
                     'variacion_del_dolar_d': round(((valor_del_dolar/data_dolar.Close.iloc[-2])-1)*100,2).item(),
                     'variacion_del_dolar_m': round(((valor_del_dolar/data_dolar.Close.iloc[dia_de_hoy])-1)*100,2).item(),
                     'variacion_del_dolar_ytd': round(((valor_del_dolar/valor_dolar_primer_dia_del_ano)-1)*100,2).item(),
                     'media_movil_21': round(media_movil_21,2).item(),
                     'media_movil_100': round(media_movil_100,2).item(),
                     'variacion_dolar_mov21': round(((media_movil_21/valor_del_dolar)-1)*100,2).item(),
                     'variacion_dolar_mov100': round(((media_movil_100/valor_del_dolar)-1)*100,2).item()
                   }
    valores_dolar = pd.DataFrame(valores_dolar, index=[0])
    return valores_dolar, emas
    
def boxplot_brechas_mep(dia_inicial, dark_mode_number, dark_mode_font):
    data_brechas, msg = calcular_brechas_dolar(dia_inicial)
    if msg is not None:
        return None, msg
    
    fig = go.Figure()

    # Obtener el último valor de cada brecha
    valor_actual_oficial_mep = data_brechas["brecha_oficial_mep"].iloc[:, 0].iloc[-1]
    valor_actual_mep_ccl = data_brechas["brecha_mep_ccl"].iloc[:, 0].iloc[-1]

    # Box plot horizontal para la brecha Oficial-MEP (sin puntos)
    fig.add_trace(go.Box(
        x=data_brechas["brecha_oficial_mep"].iloc[:, 0],
        name="Oficial - MEP",
        boxpoints=False, # Elimina los puntos de datos
    ))

    # Estrella para el valor actual de la brecha Oficial-MEP
    fig.add_trace(go.Scatter(
        x=[valor_actual_oficial_mep],
        y=["Oficial - MEP"],
        mode='markers',
        name="Valor Actual Oficial-MEP",
        marker=dict(symbol='star', size=12, color='gold'),
    ))

    # Box plot horizontal para la brecha MEP-CCL (sin puntos)
    fig.add_trace(go.Box(
        x=data_brechas["brecha_mep_ccl"].iloc[:, 0],
        name="MEP - CCL",
        boxpoints=False, # Elimina los puntos de datos
        marker_color='blueviolet'
    ))

    # Estrella para el valor actual de la brecha MEP-CCL
    fig.add_trace(go.Scatter(
        x=[valor_actual_mep_ccl],
        y=["MEP - CCL"],
        mode='markers',
        name="Valor Actual MEP-CCL",
        marker=dict(symbol='star', size=12, color='orange'),
    ))

    # Configuración de layout
    fig.update_layout(
        xaxis_title="Porcentaje (%)",
        paper_bgcolor=dark_mode_number,
        plot_bgcolor=dark_mode_number,
        font_color=dark_mode_font,
        height=230,
        margin={"t": 40, "b": 0, "l": 10, "r": 10}, # Aumenta el margen inferior
        showlegend=False,
    )
    
    # Configuración de la cuadrícula
    fig.update_layout(
        xaxis_gridcolor='rgba(255,255,255,0.4)',
        yaxis_gridcolor='rgba(255,255,255,0.4)'
    )
    
    fig.update_yaxes(autorange='reversed')

    return fig, None

def boxplot_brechas_ccl(dia_inicial, dark_mode_number, dark_mode_font):
    data_brechas, msg = calcular_brechas_dolar(dia_inicial)
    if msg is not None:
        return None, msg

    fig = go.Figure()

    # Obtener el último valor de cada brecha
    valor_actual_oficial_ccl = data_brechas["brecha_oficial_ccl"].iloc[:, 0].iloc[-1]
    valor_actual_mep_ccl = data_brechas["brecha_mep_ccl"].iloc[:, 0].iloc[-1]

    # Box plot horizontal para la brecha Oficial-MEP (sin puntos)
    fig.add_trace(go.Box(
        x=data_brechas["brecha_oficial_ccl"].iloc[:, 0],
        name="Oficial - CCL",
        boxpoints=False, # Elimina los puntos de datos
    ))

    # Estrella para el valor actual de la brecha Oficial-CCL
    fig.add_trace(go.Scatter(
        x=[valor_actual_oficial_ccl],
        y=["Oficial - CCL"],
        mode='markers',
        name="Valor Actual Oficial-CCL",
        marker=dict(symbol='star', size=12, color='gold'),
    ))

    # Box plot horizontal para la brecha MEP-CCL (sin puntos)
    fig.add_trace(go.Box(
        x=data_brechas["brecha_mep_ccl"].iloc[:, 0],
        name="MEP - CCL",
        boxpoints=False, # Elimina los puntos de datos
        marker_color='blueviolet'
    ))

    # Estrella para el valor actual de la brecha MEP-CCL
    fig.add_trace(go.Scatter(
        x=[valor_actual_mep_ccl],
        y=["MEP - CCL"],
        mode='markers',
        name="Valor Actual MEP-CCL",
        marker=dict(symbol='star', size=12, color='orange'),
    ))

    # Configuración de layout
    fig.update_layout(
        xaxis_title="Porcentaje (%)",
        paper_bgcolor=dark_mode_number,
        plot_bgcolor=dark_mode_number,
        font_color=dark_mode_font,
        height=230,
        margin={"t": 40, "b": 0, "l": 10, "r": 10}, # Aumenta el margen inferior
        showlegend=False,
    )
    
    # Configuración de la cuadrícula
    fig.update_layout(
        xaxis_gridcolor='rgba(255,255,255,0.4)',
        yaxis_gridcolor='rgba(255,255,255,0.4)'
    )
    
    fig.update_yaxes(autorange='reversed')

    return fig, None

@callback(
    [Output('grafico_del_dolar_mep_ccl', 'figure'),
    Output('brechas_mep_ccl', 'figure'),
    Output('valor_del_dolar_mep_ccl', 'children'),
    Output('variacion_del_dolar_mep_ccl_d', 'children'),
    Output('variacion_del_dolar_mep_ccl_m', 'children'),
    Output('variacion_del_dolar_mep_ccl_ytd', 'children'),
    Output('media_movil_21_mep_ccl', 'children'),
    Output('media_movil_100_mep_ccl', 'children'),
    Output('variacion_dolar_mov21_mep_ccl', 'children'),
    Output('variacion_dolar_mov100_mep_ccl', 'children'),
    Output('toast_error_dolar_mep_ccl', 'is_open'),
    Output('toast_error_dolar_mep_ccl', 'children')],
    [Input("url", "pathname"),
     Input("dark_mode", "n_clicks")])
def grafico_del_dolar_mep_ccl(path, dark_mode):
    if dark_mode is None:
        dark_mode_data = "bg-dark"  # Modo oscuro por defecto
        dark_mode_number = "#353a3f"
        dark_mode_font="white"
    elif dark_mode >= 100:
        dark_mode_data = "bg-light"  # Modo claro
        dark_mode_number = "#f9f9fa"
        dark_mode_font="#54a2e1"
    else:
        dark_mode_data = "bg-dark"  # Modo oscuro
        dark_mode_number = "#353a3f"
        dark_mode_font="white"

    primer_dia = primer_dia_habil_anual()
    valor_dolar_primer_dia_del_ano_mep, msg = calcular_dolar_mep(primer_dia)
    if msg is not None:
        return None, msg
    valor_dolar_primer_dia_del_ano_mep = valor_dolar_primer_dia_del_ano_mep.Close.iloc[0]

    valor_dolar_primer_dia_del_ano_ccl, msg = calcular_dolar_ccl(primer_dia)
    if msg is not None:
        return None, msg
    valor_dolar_primer_dia_del_ano_ccl = valor_dolar_primer_dia_del_ano_ccl.Close.iloc[0]

    # numero del dia de hoy ejemplo 2025-05-01 = 01
    dia_de_hoy = int(datetime.today().strftime('%d'))

    data_dolar, msg = calcular_brechas_dolar('2025-01-01')
    if msg is not None:
        return None, msg

    if path == "/datos_macro/dolar_mep":
        valores_dolar, emas = valores_dolar_mep_ccl(data_dolar["mep"], dia_de_hoy, valor_dolar_primer_dia_del_ano_mep)
        figCandles = grafico_de_velas_dolar_mep_ccl("mep",data_dolar["mep"], emas["dolar_EMA21"], emas["dolar_EMA100"], dark_mode_number, dark_mode_font)
        figBoxplot, msg= boxplot_brechas_mep('2025-01-01', dark_mode_number, dark_mode_font)
        if msg is not None:
            return None, None, None, None, None, None, None, None, None, None, True, msg
        
        return figCandles, figBoxplot, valores_dolar.valor_del_dolar, valores_dolar.variacion_del_dolar_d, valores_dolar.variacion_del_dolar_m, valores_dolar.variacion_del_dolar_ytd, valores_dolar.media_movil_21, valores_dolar.media_movil_100, valores_dolar.variacion_dolar_mov21, valores_dolar.variacion_dolar_mov100, False, None
    elif path == "/datos_macro/dolar_ccl":
        valores_dolar, emas = valores_dolar_mep_ccl(data_dolar["ccl"], dia_de_hoy, valor_dolar_primer_dia_del_ano_ccl)
        figCandles = grafico_de_velas_dolar_mep_ccl("ccl", data_dolar["ccl"], emas["dolar_EMA21"], emas["dolar_EMA100"], dark_mode_number, dark_mode_font)
        figBoxplot, msg = boxplot_brechas_ccl('2025-01-01', dark_mode_number, dark_mode_font)
        if msg is not None:
            return None, None, None, None, None, None, None, None, None, None, True, msg

        return figCandles, figBoxplot, valores_dolar.valor_del_dolar, valores_dolar.variacion_del_dolar_d, valores_dolar.variacion_del_dolar_m, valores_dolar.variacion_del_dolar_ytd, valores_dolar.media_movil_21, valores_dolar.media_movil_100, valores_dolar.variacion_dolar_mov21, valores_dolar.variacion_dolar_mov100, False, None
    else:
        return None, None, None, None, None, None, None, None, None, None, False, None