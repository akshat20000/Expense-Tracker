import customtkinter as ctk

class Report:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Reports", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.frame, text="Generate Monthly Report").pack(pady=10)
