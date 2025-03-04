import customtkinter as ctk

class Expense:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Add Expense", font=("Arial", 24)).pack(pady=20)
        ctk.CTkEntry(self.frame, placeholder_text="Expense Name").pack(pady=10)
        ctk.CTkEntry(self.frame, placeholder_text="Amount").pack(pady=10)
        ctk.CTkButton(self.frame, text="Add Expense").pack(pady=10)
