import customtkinter as ctk
from db.database import get_expenses
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="Expense Report", font=("Arial", 24)).pack(pady=20)
        self.create_line_graph()

    def create_line_graph(self):
        expenses = get_expenses()
        if not expenses:
            ctk.CTkLabel(self, text="No Expenses Found", font=("Arial", 16)).pack(pady=20)
            return

        dates = [expense[3] for expense in expenses]
        amounts = [expense[1] for expense in expenses]

        fig, ax = plt.subplots()
        ax.plot(dates, amounts, marker='o', linestyle='-', color='blue')
        ax.set_title("Expense Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)
        canvas.draw()