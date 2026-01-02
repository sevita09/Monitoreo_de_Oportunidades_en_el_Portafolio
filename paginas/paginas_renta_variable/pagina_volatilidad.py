from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


def pagina_volatilidad(dark_mode):
    # Single-line inputs: categoría, moneda, ticker (datalist), días, bins
    return html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                html.H5('Categoría'),
                dbc.RadioItems(
                    id='categoria_volatilidad',
                    options=[
                        {'label': 'Líder', 'value': 'Lider'},
                        {'label': 'General', 'value': 'General'},
                        {'label': 'Cedear', 'value': 'Cedear'},
                    ],
                    value='Lider',
                    inline=True,
                    className='categoria-volatilidad-radio'
                )
            ]), width={'size': 3}),

            dbc.Col(html.Div([
                html.H5('Moneda (Dólares?)'),
                daq.BooleanSwitch(id='dolares_volatilidad', on=False)
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Ticker'),
                # Input libre + Dropdown de sugerencias (escribe o selecciona)
                dcc.Input(id='ticker_volatilidad', type='text', placeholder='Escribe ticker...', style={'width': '100%'}),
                dcc.Dropdown(id='ticker_dropdown_suggestions', options=[], placeholder='Sugerencias...', clearable=True, style={'marginTop': '4px'})
            ]), width={'size': 3}),

            dbc.Col(html.Div([
                html.H5('Días'),
                dcc.Input(id='dias_volatilidad', type='number', value=500, min=50, style={'width': '100%'})
            ]), width={'size': 2}),

            dbc.Col(html.Div([
                html.H5('Bins'),
                dcc.Input(id='bins_volatilidad', type='number', value=30, min=5, style={'width': '100%'})
            ]), width={'size': 2}),
        ], style={'gap': '8px', 'marginTop': '1.0rem', 'alignItems': 'center'}),

        # Graph and stats
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_de_volatilidad", figure=None, className="grafico_de_volatilidad"), width={'size': 12, 'offset': 0}, style={'marginTop': '1.0rem'})
        ),
        # Toast para errores (se cierra automáticamente en 7s)
        dbc.Toast(id='toast_error', header='Error', is_open=False, duration=7000, dismissable=True, icon='danger', style={'position':'fixed','top':'10px','right':'10px','zIndex':9999}),
        dbc.Row([
            dbc.Col(html.H5('Desviación actual (%)'), width={'size': 3}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_actual_volatilidad', children=None), width={'size': 3}, style={'textAlign':'center'}),
            dbc.Col(html.H5('Std (hist) (%)'), width={'size': 3}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='std_volatilidad', children=None), width={'size': 3}, style={'textAlign':'center'})
        ], style={'marginTop':'15px'}),

        dbc.Row([
            dbc.Col(html.H5('Desvíos estándar (Z)'), width={'size': 3}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='z_volatilidad', children=None), width={'size': 3}, style={'textAlign':'center'}),
            dbc.Col(html.H5('Tamaño 1σ (%)'), width={'size': 3}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='std_valor_volatilidad', children=None), width={'size': 3}, style={'textAlign':'center'})
        ], style={'marginTop':'8px'}),

    ], style={"height": "100vh"}, className=dark_mode)
