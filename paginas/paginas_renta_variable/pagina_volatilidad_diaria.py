from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


# Nota: la importación de la función de descarga la hacemos dentro del callback
# para evitar problemas de resolución estática en entornos donde los paquetes
# no están configurados como módulos Python.

def pagina_volatilidad_diaria(dark_mode):
    """Página con 6 histogramas de volatilidad en diferentes ventanas."""
    # Reutilizamos los mismos IDs de inputs que la página principal para consistencia
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
                html.H5('Categoría', style={'display': 'flex', 'justifyContent': 'center'}),
                dbc.RadioItems(
                    id='categoria_volatilidad_diaria',
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
                        'justifyContent': 'center',
                        'color': 'white'
                    },
                    inline=True,
                    className='categoria-volatilidad-radio'
                )
            ]), width={'size': 2}),

            dbc.Col(html.Div([
                html.Img(id='logo_url_pagina_volatilidad_diaria', style={'height':'100px', 'width':'100px'})
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Ticker', style={'display': 'flex', 'justifyContent': 'center'}),
                dcc.Input(id='ticker_volatilidad_diaria', type='text', placeholder='Escribe ticker...', style={'width': '100%', 'textAlign': 'center'}),
                dcc.Dropdown(id='ticker_dropdown_suggestions_volatilidad_diaria', options=[], placeholder='Sugerencias...', clearable=True, style={'marginTop': '4px', 'textAlign': 'center'})
            ]), width={'size': 2}),
            
            dbc.Col(html.Div([
                html.H5('Moneda', style={'height':'40px', 'display': 'flex', 'justifyContent': 'center'}),
                daq.BooleanSwitch(id='dolares_volatilidad_diaria', label=['$', 'U$D'], style={'height':'50px', 'color': 'white'}, on=False)
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Días', style={'height':'36px', 'display': 'flex', 'justifyContent': 'center'}),
                dcc.Input(id='dias_volatilidad_diaria', value=500, style={'width': '100%', 'textAlign': 'center'}),
                html.H5(' ', style={'height':'13px'})
            ]), width={'size': 1}),

            dbc.Col(html.Div([
                html.H5('Bins', style={'height':'36px', 'display': 'flex', 'justifyContent': 'center'}),
                dcc.Input(id='bins_volatilidad_diaria', value=30, style={'width': '100%', 'textAlign': 'center'}),
                html.H5(' ', style={'height':'13px'})
            ]), width={'size': 1}),

            dbc.Col(html.Div([
            ]), width={'size': 2}),

        ], style={'width': {'size': 12, 'offset': 0}, 'marginTop': '1.0rem', 'alignItems': 'center'}),

        # Toast para errores (se cierra automáticamente en 7s)
    dbc.Toast(id='toast_error_pagina_volatilidad_diaria', header='Error', is_open=False, duration=7000, dismissable=True, icon='danger', style={'position':'fixed','top':'10px','right':'10px','zIndex':9999}),

        # Titulos para la primera fila de 3 gráficos
        dbc.Row([
            dbc.Col(html.H5(id='titulo_diaria_1_volatilidad_diaria', children='', className='text-center'), width=4),
            dbc.Col(html.H5(id='titulo_diaria_2_volatilidad_diaria', children='', className='text-center'), width=4),
            dbc.Col(html.H5(id='titulo_diaria_3_volatilidad_diaria', children='', className='text-center'), width=4),
        ], style={'marginTop':'0.6rem'}),

        # Primera fila de 3 gráficos
        dbc.Row([
            dbc.Col(dcc.Graph(id='graf_diaria_1_volatilidad_diaria', figure=None), width=4),
            dbc.Col(dcc.Graph(id='graf_diaria_2_volatilidad_diaria', figure=None), width=4),
            dbc.Col(dcc.Graph(id='graf_diaria_3_volatilidad_diaria', figure=None), width=4),
        ], style={'marginTop':'0.25rem', 'height':'180px'}),

        # Fila de cajas de estadísticas para los primeros 3 gráficos
        dbc.Row([
            dbc.Col(html.Div(id='stats_diaria_1_volatilidad_diaria', children='', style={'border':'1px solid #ddd','color': '#ddd','display':'flex','alignItems':'center','justifyContent':'center'}), width=4),
            dbc.Col(html.Div(id='stats_diaria_2_volatilidad_diaria', children='', style={'border':'1px solid #ddd','color': '#ddd','display':'flex','alignItems':'center','justifyContent':'center'}), width=4),
            dbc.Col(html.Div(id='stats_diaria_3_volatilidad_diaria', children='', style={'border':'1px solid #ddd','color': '#ddd','display':'flex','alignItems':'center','justifyContent':'center'}), width=4),
        ], style={'marginTop':'0.5rem'}),

        # Titulos para la segunda fila de 3 gráficos
        dbc.Row([
            dbc.Col(html.H5(id='titulo_diaria_4_volatilidad_diaria', children='', className='text-center'), width=4),
            dbc.Col(html.H5(id='titulo_diaria_5_volatilidad_diaria', children='', className='text-center'), width=4),
            dbc.Col(html.H5(id='titulo_diaria_6_volatilidad_diaria', children='', className='text-center'), width=4),
        ], style={'marginTop':'0.6rem'}),

        # Segunda fila de 3 gráficos
        dbc.Row([
            dbc.Col(dcc.Graph(id='graf_diaria_4_volatilidad_diaria', figure=None), width=4),
            dbc.Col(dcc.Graph(id='graf_diaria_5_volatilidad_diaria', figure=None), width=4),
            dbc.Col(dcc.Graph(id='graf_diaria_6_volatilidad_diaria', figure=None), width=4),
        ], style={'marginTop':'0.25rem', 'height':'180px'}),

        # Fila de cajas de estadísticas para los segundos 3 gráficos
        dbc.Row([
            dbc.Col(html.Div(id='stats_diaria_4_volatilidad_diaria', children='', style={'border':'1px solid #ddd','color': '#ddd','display':'flex','alignItems':'center','justifyContent':'center'}), width=4),
            dbc.Col(html.Div(id='stats_diaria_5_volatilidad_diaria', children='', style={'border':'1px solid #ddd','color': '#ddd','display':'flex','alignItems':'center','justifyContent':'center'}), width=4),
            dbc.Col(html.Div(id='stats_diaria_6_volatilidad_diaria', children='', style={'border':'1px solid #ddd','color': '#ddd','display':'flex','alignItems':'center','justifyContent':'center'}), width=4),
        ], style={'marginTop':'0.5rem'}),

    ], style={"height": "100vh", 'overflow': 'hidden'}, className=dark_mode)


