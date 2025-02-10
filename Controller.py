from dash import Input, State, Output, exceptions
import plotly.express as px

from Dashboard import Dashboard
from Portfolio import Portfolio


class Controller:
    def __init__(self):
        self.portfolio = Portfolio()
        self.dashboard = Dashboard(self.portfolio)

        self.dashboard.app.callback(
            Output('ticker_graph', 'figure'),
            Output('portfolio_table', 'data'),
            Input('add_ticker', 'n_clicks'),
            State('ticker_name', 'value'),
            State('ticker_amount', 'value'),
            State('ticker_price', 'value'),
            prevent_initial_call=True)(self.add_ticker)

    def run(self):
        self.dashboard.app.run(debug=True)

    def add_ticker(self, n_clicks, name, amount, price):
        name = name.upper()
        if name == '' or amount is None or price is None:
            raise exceptions.PreventUpdate
        if not self.portfolio.add_asset(name, amount, price):
            raise exceptions.PreventUpdate

        df = self.portfolio.get_asset_history()
        table = self.portfolio.get_portfolio().to_dict('records')

        return px.line(df, x="Date", y="Close", color="Ticker"), table
