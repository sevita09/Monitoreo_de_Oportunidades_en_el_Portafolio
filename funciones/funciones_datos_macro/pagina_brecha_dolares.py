from datetime import timedelta
from datetime import date
from dash import Input, Output, callback
import plotly.graph_objects as go
from funciones.funciones_datos_macro.pagina_dolar_mep_ccl import calcular_brechas_dolar

def boxplot_brechas_mep(data_brechas, dark_mode_number, dark_mode_font):
    fig = go.Figure()

    # Obtener el último valor de cada brecha
    valor_actual_oficial_mep = data_brechas["brecha_oficial_mep"].iloc[:, 0].iloc[-1]
    valor_actual_mep_ccl = data_brechas["brecha_mep_ccl"].iloc[:, 0].iloc[-1]
    valor_actual_oficial_ccl = data_brechas["brecha_oficial_ccl"].iloc[:, 0].iloc[-1]

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

    # Box plot horizontal para la brecha Oficial-CCL (sin puntos)
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
        marker=dict(symbol='star', size=12, color='yellow'),
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
        height=280,
        margin={"t": 40, "b": 0, "l": 10, "r": 10}, # Aumenta el margen inferior
        showlegend=False,
    )
    
    # Configuración de la cuadrícula
    fig.update_layout(
        xaxis_gridcolor='rgba(255,255,255,0.4)',
        yaxis_gridcolor='rgba(255,255,255,0.4)'
    )
    
    fig.update_yaxes(autorange='reversed')

    return fig

@callback(
    [Output('grafico_de_la_brecha_dolares', 'figure'),
    Output('brechas_dolares', 'figure'),
    Output('valor_de_la_brecha_oficial_mep', 'children'),
    Output('valor_de_la_brecha_oficial_ccl', 'children'),
    Output('valor_de_la_brecha_mep_ccl', 'children'),
    Output('valor_de_la_mediana_oficial_mep', 'children'),
    Output('valor_de_la_mediana_oficial_ccl', 'children'),
    Output('valor_de_la_mediana_mep_ccl', 'children'),
    Output('toast_error_brecha_dolares', 'is_open'),
    Output('toast_error_brecha_dolares', 'children')],
    [Input("url", "pathname"),
     Input("dark_mode", "n_clicks")])
def grafico_de_la_brecha_del_dolar(path, dark_mode):
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

    if path == "/datos_macro/brecha_dolares":
        data_brechas, msg = calcular_brechas_dolar(date.today() - timedelta(days=365*2))
        if msg is not None:
            return None, None, None, None, None, None, None, None, True, msg
        
        title_text = "Brechas entre Dólares"

        fig_boxplot = boxplot_brechas_mep(data_brechas, dark_mode_number, dark_mode_font)

        fig = go.Figure(layout=go.Layout(
                            title={'text': title_text, "y":0.97, "x":0.5, "xanchor": "center", "yanchor": "top"},
                            margin={"t": 40, "b": 10, "l": 10, "r": 10},
                            #height=500,
                            paper_bgcolor=dark_mode_number, 
                            plot_bgcolor=dark_mode_number, 
                            font_color=dark_mode_font
                                        ))

        # hacer un frafico de lineas con plotly con las brechas del dolar mep, ccl y oficial
        fig.add_trace(go.Scatter(y=data_brechas['brecha_oficial_mep'].Close,
                                 mode='lines',
                                 name='Brecha Oficial - MEP',
                                 line=dict(color='blue'))) 
        fig.add_trace(go.Scatter(y=data_brechas['brecha_oficial_ccl'].Close,
                                 mode='lines',
                                 name='Brecha Oficial - CCL',
                                 line=dict(color='red'))) 
        fig.add_trace(go.Scatter(y=data_brechas['brecha_mep_ccl'].Close,
                                 mode='lines',
                                 name='Brecha MEP - CCL',
                                 line=dict(color='purple')))
        
        fig.update_layout(xaxis_rangeslider_visible=False, 
                          paper_bgcolor=dark_mode_number, 
                          plot_bgcolor="black", 
                          font_color=dark_mode_font)
        fig.update_layout(
            xaxis_gridcolor='rgba(255,255,255,0.4)',  # Líneas de la cuadrícula en negro con 20% de opacidad
            yaxis_gridcolor='rgba(255,255,255,0.4)'   # Líneas de la cuadrícula en negro con 20% de opacidad
        )
        
        valor_oficial_mep = round(data_brechas["brecha_oficial_mep"].iloc[:, 0].iloc[-1], 2).item()
        valor_oficial_ccl = round(data_brechas["brecha_oficial_ccl"].iloc[:, 0].iloc[-1], 2).item()
        valor_mep_ccl = round(data_brechas["brecha_mep_ccl"].iloc[:, 0].iloc[-1], 2).item()

        mediana_oficial_mep = round(data_brechas["brecha_oficial_mep"].iloc[:, 0].median(), 2).item()
        mediana_oficial_ccl = round(data_brechas["brecha_oficial_ccl"].iloc[:, 0].median(), 2).item()
        mediana_mep_ccl = round(data_brechas["brecha_mep_ccl"].iloc[:, 0].median(), 2).item()

        return fig, fig_boxplot, valor_oficial_mep, valor_oficial_ccl, valor_mep_ccl, mediana_oficial_mep, mediana_oficial_ccl, mediana_mep_ccl, False, None
    else:
        return None, None, None, None, None, None, None, None, False, None