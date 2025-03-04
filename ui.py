import customtkinter as ctk

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        ctk.CTkLabel(self.frame, text="Welcome to Dashboard", font=("Arial", 24)).pack(pady=20)

class AddExpense:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        ctk.CTkLabel(self.frame, text="Add Expense", font=("Arial", 24)).pack(pady=20)

class Reports:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        ctk.CTkLabel(self.frame, text="Reports", font=("Arial", 24)).pack(pady=20)
