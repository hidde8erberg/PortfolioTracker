import pandas as pd
import yfinance as yf

class Asset:
    def __init__(self, name, quantity, purchase_price, dat):
        self.name = name
        self.purchase_price = float(purchase_price)
        self.quantity = int(quantity)

        self.sector = dat.info['sector']
        self.asset_class = dat.info['longBusinessSummary']
        self.history = dat.history(period='1y')[['Close']].reset_index()
        self.history['Ticker'] = name

        print(f'Asset {name} created')


class Portfolio:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset, quantity, price):
        dat = yf.Ticker(asset)
        if dat.history(period='1d').empty:
            print(f'Could not find data for {asset}')
            return False
        self.assets.append(Asset(asset, quantity, price, dat))
        return True

    def get_asset_history(self):
        return pd.concat([asset.history for asset in self.assets]).drop_duplicates(['Ticker', 'Date'])

    def get_portfolio(self):
        return pd.DataFrame([{'Name': asset.name, 'Sector': asset.sector, 'Asset class': asset.sector,
                              'Quantity': asset.quantity, 'Price': asset.purchase_price,
                              'Transaction value': asset.quantity*asset.purchase_price,
                              'Current value': asset.quantity*asset.history.iloc[-1]['Close']} for asset in self.assets])
