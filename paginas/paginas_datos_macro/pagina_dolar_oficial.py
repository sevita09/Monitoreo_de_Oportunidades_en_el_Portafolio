from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

def pagina_dolar_oficial(dark_mode):
    return html.Div([
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_del_dolar_oficial",
                              figure=None,
                              className="grafico_del_dolar_oficial"), 
                    width={'size': 12, 'offset': 0},
                    style={'marginTop': '1.75rem'}
                    )
        ),
        dbc.Row(
            dbc.Col(daq.BooleanSwitch(
                      id='mostrar_deciles_dolar_oficial',
                      on=False,
                      className="mostrar_deciles_dolar_oficial",
                      color=dark_mode
                      ))
        ),
        dbc.Row(
            dbc.Col(html.H4(' '),
                    width={'size': 6, 'offset': 1},
                    style={'textAlign': 'right',
                           'marginTop': '15px'}
                    )
        ),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H5('Valor del dolar'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_del_dolar_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación de hoy'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_oficial_d",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación del mes'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_oficial_m",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación YTD'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_oficial_ytd",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Media movil 21'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="media_movil_21_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la media de 21'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_mov21_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            ),
            dbc.Col(dcc.Graph(id="nivel_del_valor_del_dolar_oficial",
                    figure=None,
                    className=dark_mode),
                    width={'size': 4, 'offset': 0},
                    style={'textAlign': 'center'}),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H5('Valor de la banda superior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="banda_superior_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la banda superior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_oficial_banda_superior",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Valor de la banda inferior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="banda_inferior_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la banda inferior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_oficial_banda_inferior",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Media movil 100'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="media_movil_100_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la media de 100'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_mov100_oficial",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            )]
        ),
        # Toast para errores (se cierra automáticamente en 7s)
        dbc.Toast(id='toast_error_dolar_oficial', header='Error', is_open=False, duration=7000, dismissable=True, icon='danger', style={'position':'fixed','top':'10px','right':'10px','zIndex':9999}),
        ], 
        style={"height": "100vh", 'overflow': 'hidden'},
        className=dark_mode
      )
    