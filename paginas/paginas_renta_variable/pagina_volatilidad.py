from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


def pagina_volatilidad(dark_mode):
    # Single-line inputs: categoría, moneda, ticker (datalist), días, bins
    return html.Div([
        dbc.Row([
            
        ], style={'marginTop': '1.75rem'}),

        dbc.Row([
            dbc.Col(html.H5('Volatilidad'), width={'size': 12}, style={'textAlign':'center'}),
        ], style={'marginTop': '.5rem'}),

        dbc.Row([
            dbc.Col(html.Div([
            ]), width={'size': 2}),

            dbc.Col(html.Div([
                html.H5('Categoría'),
                dbc.RadioItems(
                    id='categoria_volatilidad',
                    options=[
                        {'label': 'Líder', 'value': 'Lider'},
                        {'label': 'General', 'value': 'General'},
                        {'label': 'Cedear', 'value': 'Cedear'},
                        {'label': 'Manual', 'value': 'Manual'}
                    ],
                    value='Lider',
                    style={
                        'display': 'grid',
                        'gridTemplateColumns': '1fr 1fr', # Dos columnas de igual ancho
                    },
                    inline=True,
                    className='categoria-volatilidad-radio'
                )
            ]), width={'size': 2}),

            dbc.Col(html.Div([
                html.Img(id='logo_url', style={'height':'100px', 'width':'100px'})
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Ticker'),
                # Input libre + Dropdown de sugerencias (escribe o selecciona)
                dcc.Input(id='ticker_volatilidad', type='text', placeholder='Escribe ticker...', style={'width': '100%'}),
                dcc.Dropdown(id='ticker_dropdown_suggestions', options=[], placeholder='Sugerencias...', clearable=True, style={'marginTop': '4px'})
            ]), width={'size': 2}),
            
            dbc.Col(html.Div([
                html.H5('Moneda'),
                daq.BooleanSwitch(id='dolares_volatilidad', label=['$', 'U$D'], on=False)
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Días'),
                dcc.Input(id='dias_volatilidad', type='number', value=500, min=50, style={'width': '100%'})
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Bins'),
                dcc.Input(id='bins_volatilidad', type='number', value=30, min=5, style={'width': '100%'})
            ]), width={'size': 1}),

            dbc.Col(html.Div([
            ]), width={'size': 2}),

        ], style={'width': {'size': 12, 'offset': 0}, 'marginTop': '1.0rem', 'alignItems': 'center'}),

        # Graph and stats
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_de_volatilidad", figure=None, className="grafico_de_volatilidad"), width={'size': 12, 'offset': 0}, style={'marginTop': '1.0rem'})
        ),
        # Toast para errores (se cierra automáticamente en 7s)
        dbc.Toast(id='toast_error', header='Error', is_open=False, duration=7000, dismissable=True, icon='danger', style={'position':'fixed','top':'10px','right':'10px','zIndex':9999}),
        
        dbc.Row([
            dbc.Col(html.H5('Media'), width={'size': 1}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_media', children=None), width={'size': 2}, style={'textAlign':'left'}),
            dbc.Col(html.H5('Actual'), width={'size': 1}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_actual_volatilidad', children=None), width={'size': 2}, style={'textAlign':'left'}),
            dbc.Col(html.H5('Tamaño σ'), width={'size': 1}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='std_volatilidad', children=None), width={'size': 2}, style={'textAlign':'left'}),
            dbc.Col(html.H5('Desvíos estándar'), width={'size': 2}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='z_volatilidad', children=None), width={'size': 1}, style={'textAlign':'left'})
        ], style={'marginTop':'25px'}),

        dbc.Row([
            dbc.Col(html.H5('-2σ'), width={'size': 1}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_menos_dos_sigma', children=None), width={'size': 2}, style={'textAlign':'left'}),
            dbc.Col(html.H5('-σ'), width={'size': 1}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_menos_sigma', children=None), width={'size': 2}, style={'textAlign':'left'}),
            dbc.Col(html.H5('σ'), width={'size': 1}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_sigma', children=None), width={'size': 2}, style={'textAlign':'left'}),
            dbc.Col(html.H5('2σ'), width={'size': 2}, style={'textAlign':'center'}),
            dbc.Col(html.H5(id='valor_dos_sigma', children=None), width={'size': 1}, style={'textAlign':'left'})
        ], style={'marginTop':'10px'}),
        
    ], style={"height": "100vh", 'overflow': 'hidden'}, className=dark_mode)
