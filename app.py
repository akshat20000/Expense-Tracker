from customtkinter import *
from sidebar import Sidebar
from auth import Auth
from dashboard import Dashboard


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("Wallet Wise")

        self.container = CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.auth = Auth(self.container, self.show_dashboard)
        self.auth.signup_screen()  # Start With Signup Screen

    def show_page(self, page, *args):
        if self.container.winfo_children():
            for widget in self.container.winfo_children():
                widget.destroy()
        page_instance = page(self.container, *args)
        page_instance.pack(fill="both", expand=True)

    def show_dashboard(self):
        if self.container.winfo_children():
            for widget in self.container.winfo_children():
                widget.destroy()
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")
        self.show_page(Dashboard, "Akshat", 5000)  # Akshat Username aur Holdings


if __name__ == "__main__":
    app = App()
    app.mainloop()
