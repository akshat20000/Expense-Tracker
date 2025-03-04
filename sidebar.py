import customtkinter as ctk
from dashboard import Dashboard
from expenses import ExpensePage
from report import ReportPage
from budget import BudgetPage
from backup import BackupPage


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, show_page):
        super().__init__(parent)
        self.show_page = show_page
        self.pack(side="left", fill="y", padx=10)
        self.configure(width=200)

        buttons = [
            ("Dashboard", Dashboard),
            ("Add Expense", ExpensePage),
            ("View Expenses", ReportPage),
            ("Set Budget", BudgetPage),
            ("Backup & Restore", BackupPage)
        ]

        for text, page in buttons:
            ctk.CTkButton(self, text=text, command=lambda p=page: self.show_page(p)).pack(pady=10)
