from dash import Input, State, Output, exceptions
import plotly.express as px

from Dashboard import Dashboard
from Portfolio import Portfolio


class Controller:
    def __init__(self):
        self.portfolio = Portfolio()
        self.dashboard = Dashboard(self.portfolio)

        self.dashboard.app.callback(
            Output("ticker_graph", "figure"),
            Output("portfolio_table", "data"),
            Output("pie_asset", "figure"),
            Output("pie_sector", "figure"),
            Output("pie_class", "figure"),
            Output("total_value", "children"),
            Output("pl_value", "children"),
            Input("add_ticker", "n_clicks"),
            State("ticker_name", "value"),
            State("ticker_amount", "value"),
            State("ticker_price", "value"))(self.add_ticker)

    def run(self):
        self.dashboard.app.run(debug=True)

    def add_ticker(self, n_clicks: int, name: str, amount: str, price: str):
        if n_clicks == 0:
            return px.line([]), [], px.pie(), px.pie(), px.pie(), "0", "0"
        name = name.upper()
        if name == "" or amount == "" or price == "":
            raise exceptions.PreventUpdate
        if not self.portfolio.add_asset(name, amount, price):
            raise exceptions.PreventUpdate

        df = self.portfolio.get_asset_history()
        table = self.portfolio.get_portfolio().to_dict("records")
        pie = self.portfolio.get_portfolio().to_dict("records")

        return (px.line(df, x="Date", y="Close", color="Ticker", title=""), table,
                px.pie(pie, names="Name", title="Assets", values="Current value").update_layout(autosize=False),
                px.pie(pie, names="Sector", title="Sectors", values="Current value").update_layout(autosize=False),
                px.pie(pie, names="Asset class", title="Asset Classes", values="Current value").update_layout(autosize=False),
                str(round(self.portfolio.get_portfolio()["Current value"].sum(), 2)),
                str(round(self.portfolio.get_portfolio()["Profit"].sum(), 2)))
