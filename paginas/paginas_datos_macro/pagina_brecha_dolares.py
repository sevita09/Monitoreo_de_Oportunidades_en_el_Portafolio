from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

def pagina_brecha_dolares(dark_mode):
    return html.Div([
        dbc.Row(
            dbc.Col(dcc.Graph(id="grafico_de_la_brecha_dolares",
                              figure=None,
                              className="grafico_de_la_brecha_dolares"), 
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
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '6px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Brecha Oficial - MEP'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_de_la_brecha_oficial_mep",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '26px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Brecha Oficial - CCL'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_de_la_brecha_oficial_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '26px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Brecha MEP - CCL'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_de_la_brecha_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            ),
            dbc.Col(dcc.Graph(id="brechas_dolares",
                    figure=None,
                    className=dark_mode),
                    width={'size': 5, 'offset': 0},
                    style={'textAlign': 'center',
                           'marginTop': '-3rem'}),
            dbc.Col([
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '6px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Mediana Oficial - MEP'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_de_la_mediana_oficial_mep",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '26px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Mediana Oficial - CCL'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_de_la_mediana_oficial_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                ),
                dbc.Row(
                    dbc.Col(html.H4(' '),
                        width={'size': 6, 'offset': 1},
                        style={'textAlign': 'right',
                            'marginTop': '26px'}
                        )
                ),
                dbc.Row([
                    dbc.Col(html.H5('Mediana MEP - CCL'),
                            width={'size': 8, 'offset': 0},
                            style={'textAlign': 'center'}),
                    dbc.Col(html.H5(id="valor_de_la_mediana_mep_ccl",
                            children=None),
                            style={'textAlign': 'center'})]
                )]
            )]
        )], 
        style={"height": "100vh", 'overflow': 'hidden'},
        className=dark_mode
      )
    