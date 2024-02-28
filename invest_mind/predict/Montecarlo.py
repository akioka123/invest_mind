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

    def __init__(self, stock, start_date, end_date, num_simulations, term):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.num_simulations = num_simulations
        self.term = term
        self.data = self.get_data()
        print(self.data)
        self.log_returns = self.get_log_returns()
        print(self.log_returns)
        self.return_mean, self.return_std = self.get_mean_std()
        print(self.return_mean, self.return_std)

    def get_data(self) -> pd.DataFrame:
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
        return np.log(self.data["close"] / self.data["close"].shift(1))

    def calc_simulated_prices(self, start_price):
        simulated_prices = np.zeros(self.num_simulations)

        for i in range(self.num_simulations):
            current_price = [start_price]
            return_rate_df = self.get_return_rate()

            for return_rate in return_rate_df:
                current_price.append(current_price[-1] * return_rate)

            simulated_prices[i] = current_price[-1]

        simulated_result_df = pd.DataFrame(simulated_prices, columns=["price"])
        simulated_result_df["profit"] = simulated_result_df["price"] - start_price

        simulated_result = dict()
        simulated_result["mean_price"] = simulated_result_df["price"].mean()
        simulated_result["std"] = simulated_result_df["profit"].std()
        simulated_result["single_sigma"] = (
            simulated_result["mean_price"] - simulated_result["std"],
            simulated_result["mean_price"] + simulated_result["std"],
        )
        simulated_result["double_sigma"] = (
            simulated_result["mean_price"] - simulated_result["std"] * 2,
            simulated_result["mean_price"] + simulated_result["std"] * 2,
        )

        print(simulated_result_df)

        return simulated_result

    def get_return_rate(self):
        rng = np.random.default_rng()
        return_rate = rng.lognormal(self.return_mean, self.return_std, self.term)

        return return_rate

    def get_mean_std(self):
        return self.log_returns.mean(), self.log_returns.std()
