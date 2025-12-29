from dash import html, dcc
import dash_bootstrap_components as dbc

def pagina_volatilidad(dark_mode):
    return html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                html.Label('Ticker'),
                dcc.Input(id='ticker_volatilidad', type='text', value='AAPL', style={'width':'100%'})
            ]), width={'size': 3}),
            dbc.Col(html.Div([
                html.Label('Días (histórico)'),
                dcc.Input(id='dias_volatilidad', type='number', value=500, min=50, style={'width':'100%'})
            ]), width={'size': 3}),
            dbc.Col(html.Div([
                html.Label('Bins (histograma)'),
                dcc.Input(id='bins_volatilidad', type='number', value=30, min=5, style={'width':'100%'})
            ]), width={'size': 2}),
        ], style={'gap':'8px', 'marginTop':'1.5rem'}),
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_de_volatilidad", figure=None, className="grafico_de_volatilidad"), width={'size': 12, 'offset': 0}, style={'marginTop': '1.5rem'})
        ),
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
