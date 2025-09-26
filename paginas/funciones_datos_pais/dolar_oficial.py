from datetime import datetime, timedelta
from dash import html, Input, Output, callback
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def bandas(dia_inicial, valor_dia_inicial, dia_de_pendiente, valor_dia_de_pendiente, distancia):
  pendiente = (valor_dia_de_pendiente - valor_dia_inicial) / (dia_de_pendiente - dia_inicial).days
  distancia_en_dias = timedelta(days=distancia)
  dia_final = dia_de_pendiente + distancia_en_dias
  valor_dia_final = valor_dia_de_pendiente + distancia * pendiente

  # Crea un rango entre dia inicial y dia final
  date_range = pd.date_range(start=dia_inicial, end=dia_final, freq='D') # 'D' for Daily

  values = []
  for date in date_range:
      # Calculate the number of days since the start date
      days_diff = (date - dia_inicial).days
      # Calculate the value with daily reduction
      value = valor_dia_inicial + days_diff * pendiente
      # Append the value to the list
      values.append(value)

  return values, dia_final

def calculo_de_todas_las_bandas(dia_inicial, valor_dia_inicial_inferior, valor_dia_inicial_superior, dia_de_pendiente, valor_dia_de_pendiente_inferior, valor_dia_de_pendiente_superior, distancia):
  # Bandas
  banda_inferior, dia_final = bandas(dia_inicial, valor_dia_inicial_inferior, dia_de_pendiente, valor_dia_de_pendiente_inferior, distancia)
  banda_superior, dia_final = bandas(dia_inicial, valor_dia_inicial_superior, dia_de_pendiente, valor_dia_de_pendiente_superior, distancia)
  mitad_del_cono, dia_final = bandas(dia_inicial, 1200, dia_de_pendiente, 1200, distancia)

  bandas_intermedias = []

  for i in range(0,9):
    valor_inicial_decimos = (valor_dia_inicial_superior-valor_dia_inicial_inferior)/10 * (i + 1) + valor_dia_inicial_inferior
    valor_pendiente_decimos = (valor_dia_de_pendiente_superior-valor_dia_de_pendiente_inferior)/10 * (i + 1) + valor_dia_de_pendiente_inferior
    banda_decimo, dia_final = bandas(dia_inicial, valor_inicial_decimos, dia_de_pendiente, valor_pendiente_decimos, distancia)

    bandas_intermedias.append(banda_decimo)

  # Crea un rango entre dia inicial y dia final
  date_range = pd.date_range(start=dia_inicial, end=dia_final, freq='D') # 'D' for Daily

  # Create a DataFrame
  data_bandas = {'Date': date_range, 'banda_inferior': banda_inferior, 'mitad_del_cono': mitad_del_cono,'banda_superior': banda_superior}
  for i in range(0,9):
    data_bandas['banda_intermedia_'+str(i)] = bandas_intermedias[i]

  data_bandas = pd.DataFrame(data_bandas)
  return data_bandas

def valores_de_hoy_calculados(data_dolar, data_bandas):
  today = str(pd.Timestamp.today().date())
  valores_dolar = {'valor_del_dolar': round(data_dolar.Close.iloc[-1],2).item(),
                   'valor_banda_superior': round(data_bandas[data_bandas.Date == today].banda_superior.iloc[0],2).item(),
                   'valor_banda_inferior': round(data_bandas[data_bandas.Date == today].banda_inferior.iloc[0],2).item(),
                   'valor_mitad_del_cono': round(data_bandas[data_bandas.Date == today].mitad_del_cono.iloc[0],2).item(),
                   }
  for i in range(0,9):
      valores_dolar['valor_banda_intermedia_'+str(i)] = round(data_bandas[data_bandas.Date == today]['banda_intermedia_'+str(i)].iloc[0],2).item()
  valores_dolar = pd.DataFrame(valores_dolar, index=[0])

  return valores_dolar

@callback(
    [Output('grafico_del_dolar', 'figure'),
    Output('nivel_del_valor_del_dolar', 'figure'),
    Output('valor_del_dolar', 'children'),
    Output('variacion_del_dolar_d', 'children'),
    Output('variacion_del_dolar_m', 'children'),
    Output('variacion_del_dolar_ytd', 'children'),
    Output('banda_superior', 'children'),
    Output('banda_inferior', 'children'),
    Output('variacion_dolar_banda_superior', 'children'),
    Output('variacion_dolar_banda_inferior', 'children'),
    Output('media_movil_21', 'children'),
    Output('media_movil_100', 'children'),
    Output('variacion_dolar_mov21', 'children'),
    Output('variacion_dolar_mov100', 'children')],
    [Input('pagina_datos_del_pais', 'children'),
     Input('mostrar_deciles_dolar_oficial', 'on')])
def grafico_del_dolar(child, mostrar_deciles):
  if child != html.Div():
    # Obtener datos del dolar
    dolar = "USDARS=X"

    # Valores fijos para calcular pendiente
    dia_inicial = pd.to_datetime('2025-04-01')
    valor_dia_inicial_inferior = 1002.773
    valor_dia_inicial_superior = 1400.478
    dia_de_pendiente = pd.to_datetime('2025-05-01')
    valor_dia_de_pendiente_inferior = 989.337
    valor_dia_de_pendiente_superior = 1413.914
    valor_dolar_primer_dia_del_ano = yf.download(dolar, start='2025-01-02', end='2025-01-03', multi_level_index=False).Close.iloc[0]

    # Variable de día máximo del gráfico
    distancia = (pd.Timestamp.today() - dia_inicial).days

    # numero del dia de hoy ejemplo 2025-05-01 = 01
    dia_de_hoy = int(datetime.today().strftime('%d'))

    # Dolar
    data_dolar = yf.download(dolar, start=dia_inicial, multi_level_index=False)

    # Bandas
    data_bandas = calculo_de_todas_las_bandas(dia_inicial, valor_dia_inicial_inferior, valor_dia_inicial_superior, dia_de_pendiente, valor_dia_de_pendiente_inferior, valor_dia_de_pendiente_superior, distancia)

    # Serie de ema de 200 y 100 sobre el dolar
    dolar_EMA21 = data_dolar['Close'].ewm(span=21, adjust=False).mean()
    dolar_EMA100 = data_dolar['Close'].ewm(span=100, adjust=False).mean()

    # Gráfico
    figCandles = go.Figure(data=[go.Candlestick(x=data_dolar.index,
                                        open=data_dolar.Open,
                                        high=data_dolar.High,
                                        low=data_dolar.Low,
                                        close=data_dolar.Close,
                                        increasing=dict(line=dict(color='#00FF00', width=3)), # Vela verde para subir
                                        decreasing=dict(line=dict(color='#FF0000', width=3)), # Vela roja para bajar
                                        opacity=1,
                                        name='Dolar Oficial'
                                        )])
    figCandles.add_trace(go.Scatter(x=data_bandas.Date, y=data_bandas.banda_inferior, mode='lines', name='banda inferior', line=dict(color='green')))
    figCandles.add_trace(go.Scatter(x=data_bandas.Date, y=data_bandas.mitad_del_cono, mode='markers', name='mitad del cono', opacity=0.4, line=dict(color='blue')))
    figCandles.add_trace(go.Scatter(x=data_bandas.Date, y=data_bandas.banda_superior, mode='lines', name='banda superior', line=dict(color='red')))
    figCandles.add_trace(go.Scatter(x=data_dolar.index, y=dolar_EMA21, mode='lines', name='EMA 21', line=dict(color='orange', width=1)))
    figCandles.add_trace(go.Scatter(x=data_dolar.index, y=dolar_EMA100, mode='lines', name='EMA 100', line=dict(color='purple', width=1)))
    if mostrar_deciles:
      # Agregar las bandas al gráfico
      for i in range(0,9):
        figCandles.add_trace(go.Scatter(x=data_bandas.Date, y=data_bandas['banda_intermedia_'+str(i)], mode='lines', name='decil '+str(i+1), line=dict(color='yellow')))
    figCandles.update_layout(title='Dolar Oficial', xaxis_rangeslider_visible=False, template="plotly_dark")

    # valores
    valores_de_hoy = valores_de_hoy_calculados(data_dolar, data_bandas)
    variacion_del_dolar_d = ((valores_de_hoy.valor_del_dolar/data_dolar.Close.iloc[-2])-1)*100
    dia_de_hoy = -(dia_de_hoy+1)
    variacion_del_dolar_m = ((valores_de_hoy.valor_del_dolar/data_dolar.Close.iloc[dia_de_hoy])-1)*100
    variacion_del_dolar_ytd = ((valores_de_hoy.valor_del_dolar/valor_dolar_primer_dia_del_ano)-1)*100
    variacion_dolar_banda_superior = ((valores_de_hoy.valor_banda_superior/valores_de_hoy.valor_del_dolar)-1)*100
    variacion_dolar_banda_inferior = ((valores_de_hoy.valor_banda_inferior/valores_de_hoy.valor_del_dolar)-1)*100
    media_movil_21 = data_dolar.Close.rolling(window=21).mean().iloc[-1]
    media_movil_100 = data_dolar.Close.rolling(window=100).mean().iloc[-1]
    variacion_dolar_mov21 = ((media_movil_21/valores_de_hoy.valor_del_dolar)-1)*100
    variacion_dolar_mov100 = ((media_movil_100/valores_de_hoy.valor_del_dolar)-1)*100

    # Lista de 10 códigos de colores rgb en exa del rojo al verde pasando por
    # el amarillo como si fuera un semaforo
    colores = ['#33FF00', '#66FF00', '#99FF00', '#CCFF00', '#FFFF00', '#FFCC00', '#FF9900', '#FF6600', '#FF3300', '#FF0000']

    figCaro = go.Figure(go.Indicator(
      mode="gauge+number",
      value=valores_de_hoy.valor_del_dolar.iloc[0],
      number={"font": {"size": 60}},
      gauge={
          "axis": {"range": [valores_de_hoy.valor_banda_inferior.iloc[0], valores_de_hoy.valor_banda_superior.iloc[0]]},
          "bar": {"color": "rgba(0,0,0,0.5)"},
          "steps": [
              {"range": [valores_de_hoy.valor_banda_inferior.iloc[0], valores_de_hoy.valor_banda_intermedia_0.iloc[0]], "color": colores[0]},
              {"range": [valores_de_hoy.valor_banda_intermedia_0.iloc[0], valores_de_hoy.valor_banda_intermedia_1.iloc[0]], "color": colores[1]},
              {"range": [valores_de_hoy.valor_banda_intermedia_1.iloc[0], valores_de_hoy.valor_banda_intermedia_2.iloc[0]], "color": colores[2]},
              {"range": [valores_de_hoy.valor_banda_intermedia_2.iloc[0], valores_de_hoy.valor_banda_intermedia_3.iloc[0]], "color": colores[3]},
              {"range": [valores_de_hoy.valor_banda_intermedia_3.iloc[0], valores_de_hoy.valor_banda_intermedia_4.iloc[0]], "color": colores[4]},
              {"range": [valores_de_hoy.valor_banda_intermedia_4.iloc[0], valores_de_hoy.valor_banda_intermedia_5.iloc[0]], "color": colores[5]},
              {"range": [valores_de_hoy.valor_banda_intermedia_5.iloc[0], valores_de_hoy.valor_banda_intermedia_6.iloc[0]], "color": colores[6]},
              {"range": [valores_de_hoy.valor_banda_intermedia_6.iloc[0], valores_de_hoy.valor_banda_intermedia_7.iloc[0]], "color": colores[7]},
              {"range": [valores_de_hoy.valor_banda_intermedia_7.iloc[0], valores_de_hoy.valor_banda_intermedia_8.iloc[0]], "color": colores[8]},
              {"range": [valores_de_hoy.valor_banda_intermedia_8.iloc[0], valores_de_hoy.valor_banda_superior.iloc[0]], "color": colores[9]}
          ],
          "threshold": {
              "line": {"color": "black", "width": 1},
              "thickness": 0.75,
              "value": valores_de_hoy.valor_del_dolar.iloc[0]
          }
        }
      ))
    figCaro.update_layout(
    title={"text": "<b>Atraso & Devaluación Index</b>", "y": 0.45, "x": 0.5, "font": {"size": 22},},
    margin={"t": 80},
    annotations=[
        dict(x=0.5, y=0.2, text="Valor Dolar Oficial", showarrow=False, font={"size": 20}),
        dict(x=0.12, y=-0.1, text="<b>Comprar</b>",    showarrow=False, font={"size": 20}),
        dict(x=0.87, y=-0.1, text="<b>Vender</b>",    showarrow=False, font={"size": 20}),
        dict(x=0.13, y=-0.15, text="Dolar baratito",    showarrow=False, font={"size": 12}),
        dict(x=0.88, y=-0.15, text="Dolar muy caro",    showarrow=False, font={"size": 12}),

        ],
    template="plotly_dark"
    )



    return figCandles, figCaro, round(valores_de_hoy.valor_del_dolar, 2), round(variacion_del_dolar_d, 2), round(variacion_del_dolar_m, 2), round(variacion_del_dolar_ytd, 2), valores_de_hoy.valor_banda_superior.iloc[0], valores_de_hoy.valor_banda_inferior.iloc[0], round(variacion_dolar_banda_superior, 2), round(variacion_dolar_banda_inferior, 2), round(media_movil_21,2), round(media_movil_100,2), round(variacion_dolar_mov21,2), round(variacion_dolar_mov100,2)
  else:
    return None, None, None, None, None, None, None, None, None, None, None, None, None, None