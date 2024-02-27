import pandas as pd
import numpy as np


class MonteCarlo:
    column_names = [
        "open",
        "high",
        "cheap",
        "close",
        "avg_5",
        "avg_25",
        "avg_75",
        "VWAP",
        "amount",
        "amount_avg_5",
        "amount_avg_25",
    ]

    def __init__(self, stock, start_date, end_date, num_simulations):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.num_simulations = num_simulations
        self.data = self.get_data()
        self.log_returns = self.get_log_returns()
        self.simulated_prices = self.get_simulated_prices()
        self.mean, self.std = self.get_mean_std()
        self.simulated_returns = self.get_simulated_returns()
        self.simulated_portfolios = self.get_simulated_portfolios()

    def get_data(self):
        df = pd.read_csv(
            f"csv/{self.stock}_{self.start_date}_{self.end_date}.csv",
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

    def get_log_returns(self):
        return np.log(1 + self.data["close"].pct_change())

    def get_simulated_prices(self):
        simulated_prices = pd.DataFrame()
        for i in range(self.num_simulations):
            simulated_prices[i] = self.data["close"].iloc[-1] * np.exp(
                self.log_returns.mean()
                + self.log_returns.std() * np.random.normal(0, 1, len(self.data))
            )

        return simulated_prices

    def get_mean_std(self):
        return self.log_returns.mean(), self.log_returns.std()

    def get_simulated_returns(self):
        return np.log(1 + self.simulated_prices.pct_change())

    def get_simulated_portfolios(self):
        simulated_portfolios = pd.DataFrame()
        for i in range(self.num_simulations):
            simulated_portfolios[i] = self.data["close"].iloc[-1] * np.exp(
                self.mean + self.std * np.random.normal(0, 1, len(self.data))
            )

        return simulated_portfolios

    def get_simulated_portfolio_returns(self):
        return np.log(1 + self.simulated_portfolios.pct_change())
