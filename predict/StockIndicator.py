import pandas as pd
import numpy as np

from invest_mind import const


class StockIndicator:
    column_names = const.COLUMN_NAMES

    def __init__(self, stock):
        self.stock = stock
        self.data = self.get_data()

    def get_data(self):
        df = pd.read_csv(
            f"csv/{self.stock}.csv",
            index_col="日付",
            parse_dates=True,
            encoding="SJIS",
        )

        df.sort_index(inplace=True)

        df.index.name = "date"
        df.columns = self.column_names
        for name in self.column_names:
            if df[name].dtype == "O":
                df[name] = (
                    df[name].str.replace(",", "").replace("--", "0").astype(float)
                )

        return df

    def get_indicator(self):
        return self.stock.get_price() / self.stock.get_eps()
