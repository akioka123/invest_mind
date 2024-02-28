import tkinter as tk
import re
from logger.logger import AppLogger
from predict.Montecarlo import MonteCarlo


class InvestMind(tk.Tk):
    def __init__(self):
        """Initializes the InvestMind application."""
        super().__init__()
        self.logger = AppLogger("InvestMind")
        self.title("InvestMind")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the application."""
        self.message_label = tk.Label(self, text="")
        self.message_label.pack(pady=10)

        self.label = tk.Label(self, text="Welcome to InvestMind!")
        self.label.pack(pady=10)

        self.start_price_entry = self.create_input_frame("Start Price")
        self.start_date_entry = self.create_input_frame("Start Date")
        self.end_date_entry = self.create_input_frame("End Date")

        self.button = tk.Button(
            self, text="Start Montecarlo", command=self.predict_montecarlo
        )
        self.button.pack(pady=10)

        self.price_label = tk.Label(self, text="Price: ")
        self.price_label.pack(pady=10)

    def predict_montecarlo(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        regex = re.compile(r"\d{8}")
        if not regex.fullmatch(start_date) and not regex.fullmatch(end_date):
            self.logger.error("Invalid date format")
            return

        montecarlo = MonteCarlo("6768", start_date, end_date, 1000, 252)
        simulated_prices = montecarlo.get_simulated_prices(1000)
        self.price_label["text"] = f"Price: {simulated_prices.mean()}"

    def create_input_frame(self, label_name):
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text=f"{label_name}:").grid(row=0, column=0)
        entry = tk.Entry(input_frame, width=30)
        entry.grid(row=0, column=1)
        return entry


if __name__ == "__main__":
    InvestMind().mainloop()
