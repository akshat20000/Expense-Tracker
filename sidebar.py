import customtkinter as ctk
from dashboard import Dashboard
from expenses import Expense
from report import Report

class Sidebar:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, width=200, height=600, corner_radius=0)
        self.frame.pack(side="left", fill="y")
        self.create_buttons(parent)

    def create_buttons(self, parent):
        ctk.CTkButton(self.frame, text="Dashboard", command=lambda: Dashboard(parent)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Add Expense", command=lambda: Expense(parent)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Reports", command=lambda: Report(parent)).pack(pady=10)
