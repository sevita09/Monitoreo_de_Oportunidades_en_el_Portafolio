from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

def pagina_dolar_mep_ccl(dark_mode):
    return html.Div([
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_del_dolar_mep_ccl",
                              figure=None,
                              className="grafico_del_dolar_mep_ccl"), 
                    width={'size': 12, 'offset': 0},
                    style={'marginTop': '1.75rem'}
                    )
        ),
        dbc.Row(
            dbc.Col(html.H4(' '),
                    width={'size': 6, 'offset': 1},
                    style={'textAlign': 'right',
                           'marginTop': '35px'}
                    )
        ),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H5('Valor del dolar'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_del_dolar_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación de hoy'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_mep_ccl_d",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '20px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación del mes'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_mep_ccl_m",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Variación YTD'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_del_dolar_mep_ccl_ytd",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            ),
            dbc.Col(dcc.Graph(id="brechas_mep_ccl",
                    figure=None,
                    className=dark_mode),
                    width={'size': 5, 'offset': 0},
                    style={'textAlign': 'center',
                           'marginTop': '-3rem'}),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H5('Media movil 21'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="media_movil_21_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) media de 21'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_mov21_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '20px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Media movil 100'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="media_movil_100_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row([
                    dbc.Col(html.H5('Distancia(%) media de 100'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="variacion_dolar_mov100_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            )]
        )], 
        style={
            "height": "100vh"},
        className=dark_mode
      )
    