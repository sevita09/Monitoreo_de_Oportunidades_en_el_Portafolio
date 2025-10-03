from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

def pagina_datos_del_dolar_oficial(dark_mode):
    return html.Div([
        dbc.Row(
            dbc.Col(html.H4('Dolar oficial'),
                    width={'size': 6, 'offset': 1},
                    style={'textAlign': 'right',
                           'marginTop': '15px'}
                    )
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_del_dolar",
                              figure=None,
                              className="grafico_del_dolar"), 
                    width={'size': 12, 'offset': 0}
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
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H5('Valor del dolar'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_del_dolar",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación de hoy'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_d",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación del mes'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_m",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación YTD'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_ytd",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Media movil 21'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="media_movil_21",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la media de 21'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_mov21",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            ),
            dbc.Col(dcc.Graph(id="nivel_del_valor_del_dolar",
                    figure=None,
                    className=dark_mode),
                    width={'size': 4, 'offset': 0},
                    style={'textAlign': 'center'}),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H5('Valor de la banda superior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="banda_superior",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la banda superior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_banda_superior",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Valor de la banda inferior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="banda_inferior",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la banda inferior'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_banda_inferior",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Media movil 100'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="media_movil_100",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) a la media de 100'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_mov100",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            )]
        )], 
        style={"height": "100vh"},
        className=dark_mode
      )
    