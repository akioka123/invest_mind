import tkinter as tk


class InvestMind(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InvestMind")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to InvestMind!")
        self.label.pack(pady=10)
        self.button = tk.Button(self, text="Start", command=self.start)
        self.button.pack(pady=10)

    def start(self):
        # Add your code here
        pass


if __name__ == "__main__":
    InvestMind().mainloop()
