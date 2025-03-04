from Sidebar import Sidebar
import customtkinter as ctk

ctk.set_appearance_mode("light")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wallet App - Expense Tracker & Budget Manager")
        self.geometry("1200x700")

        self.sidebar = Sidebar(self)
        self.sidebar.show_page(Dashboard)  # Default Page Load

if __name__ == "__main__":
    app = App()
    app.mainloop()
