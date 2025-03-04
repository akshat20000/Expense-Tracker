from customtkinter import *

class Dashboard(CTkFrame):
    def __init__(self, parent, username, current_holdings):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        
        # Welcome message with username
        self.welcome_label = CTkLabel(self, text=f"Welcome, {username}!", font=("Arial", 24))
        self.welcome_label.pack(pady=20)
        
        # Display current holdings
        self.holdings_label = CTkLabel(self, text=f"Current Holdings: ₹{current_holdings}", font=("Arial", 20))
        self.holdings_label.pack(pady=10)

        # Placeholder for future widgets
        self.info_label = CTkLabel(self, text="Your financial summary will appear here.", font=("Arial", 16))
        self.info_label.pack(pady=20)

if __name__ == "__main__":
    root = CTk()
    root.geometry("1200x700")
    Dashboard(root, "Akshat", 5000).pack(fill="both", expand=True)
    root.mainloop()
