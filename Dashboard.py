from dash import Dash, html, dcc, dash_table


class Dashboard:
    def __init__(self, portfolio):
        self.app = Dash()
        self.app.layout = [html.Div(children='Add a new asset'),
                           html.Div(dcc.Input(
                              id="ticker_name".format("text"),
                              type="text",
                              placeholder="Name".format("text"))),
                           html.Div(dcc.Input(
                              id="ticker_amount".format("number"),
                              type="number",
                              placeholder="Amount".format("number"))),
                           html.Div(dcc.Input(
                              id="ticker_price".format("text"),
                              type="text",
                              placeholder="Price".format("text"))),
                           html.Button('ADD TICKER', id='add_ticker', n_clicks=0),
                           dcc.Graph(id="ticker_graph"),
                           dash_table.DataTable(id='portfolio_table')]

