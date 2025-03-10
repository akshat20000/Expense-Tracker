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

    def display_user_info(self):
        self.user_info = CTkLabel(self, text=f"User: {self.welcome_label.cget('text').split(', ')[-1]}", font=("Arial", 18))
        self.user_info.pack(pady=10)
        self.holdings_info = CTkLabel(self, text=f"Holdings: {self.holdings_label.cget('text').split(': ')[-1]}", font=("Arial", 18))
        self.holdings_info.pack(pady=10)

    def update_user_info(self, username, current_holdings):
        self.welcome_label.configure(text=f"Welcome, {username}!")
        self.holdings_label.configure(text=f"Current Holdings: ₹{current_holdings}")
        self.user_info.configure(text=f"User: {username}")
        self.holdings_info.configure(text=f"Holdings: ₹{current_holdings}")

if __name__ == "__main__":
    root = CTk()
    root.geometry("1200x700")
    dashboard = Dashboard(root, "Akshat", 5000)
    dashboard.pack(fill="both", expand=True)
    dashboard.display_user_info()
    root.mainloop()
