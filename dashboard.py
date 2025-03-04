import customtkinter as ctk

class Dashboard:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Dashboard", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.frame, text="View Expenses").pack(pady=10)
        ctk.CTkButton(self.frame, text="Set Budget").pack(pady=10)
        ctk.CTkButton(self.frame, text="Generate Report").pack(pady=10)
