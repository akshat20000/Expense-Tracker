import customtkinter as ctk


class BudgetPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Set Your Budget", font=("Arial", 24)).pack(pady=20)
