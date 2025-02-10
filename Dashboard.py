from dash import Dash, html, dcc, dash_table


class Dashboard:
    def __init__(self, portfolio):
        self.app = Dash()
        self.app.layout = [
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        # 'Add a new asset',
                        html.Div(dcc.Input(
                          id="ticker_name".format("text"),
                          type="text",
                          placeholder="Name".format("text"))),
                        html.Div(dcc.Input(
                          id="ticker_amount".format("text"),
                          type="text",
                          placeholder="Amount".format("text"))),
                        html.Div(dcc.Input(
                          id="ticker_price".format("text"),
                          type="text",
                          placeholder="Price".format("text"))),
                        html.Button('ADD ASSET', id='add_ticker', n_clicks=0),
                        html.H2("Total Portfolio Value", style={'marginBottom': '0px'}),
                        html.H2(id="total_value")
                    ], style={'width': '15%', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
                    dcc.Graph(id="ticker_graph", style={'width': '70%', 'height': '40vh'}),
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Div(children=[
                    dcc.Graph(id="pie_asset", style={"width": "30%", 'height': "30vh"}),
                    dcc.Graph(id="pie_sector", style={"width": "30%"}),
                    dcc.Graph(id="pie_class", style={"width": "30%"})
                ], style={"display": "flex", "justifyContent": "center"}),
                dash_table.DataTable(id='portfolio_table', page_action='none',
                                     sort_action="native",
                                     style_table={'width': '90%', "margin": "auto", 'height': '300px', 'overflowY': 'auto'}),

            ])
        ]

