from customtkinter import *
from sidebar import Sidebar
from auth import Auth
from dashboard import Dashboard


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("Akshat Pay™")

        self.container = CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.auth = Auth(self.container, self.show_dashboard)
        self.auth.signup_screen()  # Start With Signup Screen

    def show_page(self, page):
        for widget in self.container.winfo_children():
            widget.destroy()
        page(self.container).pack(fill="both", expand=True)

    def show_dashboard(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")
        self.show_page(Dashboard)


if __name__ == "__main__":
    app = App()
    app.mainloop()
