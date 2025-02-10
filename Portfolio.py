import pandas as pd
import yfinance as yf


class Asset:
    def __init__(self, name: str, quantity: str, purchase_price: str, dat):
        self.name = name
        self.purchase_price = float(purchase_price)
        self.quantity = float(quantity)

        self.sector = dat.info.get('sector', 'Unknown')
        self.asset_class = dat.info.get('quoteType', 'Unknown') # classify_asset_class(self.sector)
        self.history = dat.history(period='1y')[['Close']].reset_index()
        self.history['Ticker'] = name

        print(f'Asset {name} created')


class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset: str, quantity: str, price: str) -> bool:
        dat = yf.Ticker(asset)
        if dat.history(period='1d').empty:
            print(f'Could not find data for {asset}')
            return False
        self.assets.append(Asset(asset, quantity, price, dat))
        return True

    def get_asset_history(self):
        return pd.concat([asset.history for asset in self.assets]).drop_duplicates(['Ticker', 'Date'])

    def get_portfolio(self):
        return pd.DataFrame([{'Name': asset.name, 'Sector': asset.sector, 'Asset class': asset.asset_class,
                              'Quantity': asset.quantity, 'Price': asset.purchase_price,
                              'Transaction value': asset.quantity*asset.purchase_price,
                              'Current value': round(asset.quantity*asset.history.iloc[-1]['Close'], 2)} for asset in self.assets])
