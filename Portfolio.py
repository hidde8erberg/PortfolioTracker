import pandas as pd
import yfinance as yf


class Asset:
    def __init__(self, name: str, quantity: str, purchase_price: str, dat):
        self.name = name
        self.purchase_price = float(purchase_price)
        self.quantity = float(quantity)

        self.sector = dat.info.get("sector", "Unknown")
        self.asset_class = dat.info.get("quoteType", "Unknown") # classify_asset_class(self.sector)
        self.history = dat.history(period="1y")[["Close"]].reset_index()
        self.history["Ticker"] = name

        print(f"Asset {name} created")


class Portfolio:
    def __init__(self):
        self.assets = []
        # self.add_from_file()

    def add_asset(self, asset: str, quantity: str, price: str) -> bool:
        dat = yf.Ticker(asset)
        if dat.history(period="1d").empty:
            print(f"Could not find data for {asset}")
            return False
        self.assets.append(Asset(asset, quantity, price, dat))
        return True

    def get_asset_history(self):
        return pd.concat([asset.history for asset in self.assets]).drop_duplicates(["Ticker", "Date"])

    def get_portfolio(self):
        return pd.DataFrame([{"Name": asset.name, "Sector": asset.sector, "Asset class": asset.asset_class,
                              "Quantity": asset.quantity, "Price": asset.purchase_price,
                              "Transaction value": asset.quantity*asset.purchase_price,
                              "Current value": round(asset.quantity*asset.history.iloc[-1]["Close"], 2),
                              "Profit": round(asset.quantity*asset.history.iloc[-1]["Close"] - asset.quantity*asset.purchase_price, 2),
                              } for asset in self.assets])

    def save_to_file(self, n_clicks: int):
        df = pd.DataFrame([asset.__dict__ for asset in self.assets])
        df.to_csv("assets.csv", index=False)

    def add_from_file(self):
        print("Initializing Portfolio and loading assets from file...")
        df = pd.read_csv("assets.csv")
        for _, row in df.iterrows():
            self.add_asset(row["name"], row["quantity"], row["purchase_price"])

