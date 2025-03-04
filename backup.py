import customtkinter as ctk


class BackupPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        ctk.CTkButton(self, text="Backup").pack(pady=10)
        ctk.CTkButton(self, text="Restore").pack(pady=10)
