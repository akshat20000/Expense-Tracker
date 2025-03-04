import customtkinter as ctk
from PIL import Image, ImageTk
from database import add_expense, get_expenses, delete_expense, edit_expense
import sqlite3
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib

# App Configuration
ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("900x600")
app.title("Wallet App - Expense Tracker & Budget Manager")

class Auth:
    def __init__(self):
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()
        self.create_users_table()
        self.logged_in_user = None

    def create_users_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def signup(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            self.conn.commit()
            self.login_screen()
        except sqlite3.IntegrityError:
            print("Username already exists!")

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            self.logged_in_user = user[1]
            self.show_dashboard()
        else:
            print("Invalid username or password!")

    def login_screen(self):
        for widget in app.winfo_children():
            widget.destroy()
        ctk.CTkLabel(app, text="Login", font=("Arial", 24)).pack(pady=20)
        username = ctk.CTkEntry(app, placeholder_text="Username")
        username.pack(pady=5)
        password = ctk.CTkEntry(app, placeholder_text="Password", show="*")
        password.pack(pady=5)
        ctk.CTkButton(app, text="Login", command=lambda: self.login(username.get(), password.get())).pack(pady=10)
        ctk.CTkButton(app, text="Signup", command=self.signup_screen).pack(pady=5)

    def signup_screen(self):
        for widget in app.winfo_children():
            widget.destroy()
        ctk.CTkLabel(app, text="Signup", font=("Arial", 24)).pack(pady=20)
        username = ctk.CTkEntry(app, placeholder_text="Username")
        username.pack(pady=5)
        password = ctk.CTkEntry(app, placeholder_text="Password", show="*")
        password.pack(pady=5)
        ctk.CTkButton(app, text="Signup", command=lambda: self.signup(username.get(), password.get())).pack(pady=10)
        ctk.CTkButton(app, text="Go to Login", command=self.login_screen).pack(pady=5)

    def show_dashboard(self):
        for widget in app.winfo_children():
            widget.destroy()
        Sidebar(app)
        ExpenseTable(app)
        Dashboard(app)

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#D3D3D3")
        self.pack(fill="both", expand=True)

        # Header
        title = ctk.CTkLabel(self, text="Dashboard", font=("Poppins", 30, "bold"))
        title.pack(pady=20)

        # Balance Card
        balance_card = ctk.CTkFrame(self, height=150, corner_radius=20, fg_color="#1E90FF")
        balance_card.pack(pady=20, padx=40, fill="x")

        balance_label = ctk.CTkLabel(balance_card, text="Total Balance", font=("Poppins", 20, "bold"), text_color="white")
        balance_label.pack(pady=10)

        balance_amount = ctk.CTkLabel(balance_card, text="₹ 0.00", font=("Poppins", 40, "bold"), text_color="white")
        balance_amount.pack()

        # Recent Transactions
        recent_label = ctk.CTkLabel(self, text="Recent Transactions", font=("Poppins", 20, "bold"))
        recent_label.pack(pady=10)

        self.recent_list = ctk.CTkListbox(self, height=200, width=400)
        self.recent_list.pack(pady=10)


class Sidebar:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, width=200, height=600, corner_radius=0)
        self.frame.pack(side="left", fill="y")
        self.is_collapsed = False
        self.current_page = None  # To Store Current Active Page
        self.pack(fill="both", expand=True)

        self.create_buttons()

        self.toggle_button = ctk.CTkButton(self.frame, text="Toggle", command=self.toggle_sidebar)
        self.toggle_button.pack(side="bottom", pady=10)

    def create_buttons(self):
        ctk.CTkButton(self.frame, text="Dashboard", command=lambda: self.show_page(Dashboard)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Add Expense", command=lambda: self.show_page(AddExpense)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Reports", command=lambda: self.show_page(Report)).pack(pady=10)

    def show_page(self, page_class):
        if self.current_page is not None:
            self.slide_out(self.current_page)  # Old Page Slide Out Animation
            self.current_page.destroy()

        self.current_page = page_class(self.parent)
        self.current_page.pack(fill="both", expand=True)

        self.slide_in(self.current_page)  # New Page Slide In Animation

    def slide_in(self, widget):
        widget.place(x=1000, y=0)  # Start from Right Side
        for x in range(1000, 0, -20):
            widget.place(x=x, y=0)
            widget.update()

    def slide_out(self, widget):
        for x in range(0, -1000, -20):
            widget.place(x=x, y=0)
            widget.update()

    def toggle_sidebar(self):
        if self.is_collapsed:
            self.frame.configure(width=200)
            self.is_collapsed = False
        else:
            self.frame.configure(width=0)
            self.is_collapsed = True


class ExpenseTable:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(side="right", fill="both", expand=True)
        ctk.CTkLabel(self.frame, text="Expense History", font=("Arial", 24)).pack(pady=20)
        self.display_table()
        self.pack(fill="both", expand=True)

    def display_table(self):
        expenses = get_expenses()
        for expense in expenses:
            text = f"{expense[3]} | {expense[2]} | {expense[1]} Rs | {expense[4]}"
            row = ctk.CTkFrame(self.frame)
            row.pack(pady=5, fill="x")
            ctk.CTkLabel(row, text=text, font=("Arial", 16)).pack(side="left")
            ctk.CTkButton(row, text="Edit", command=lambda e=expense: self.edit_expense(e)).pack(side="right")
            ctk.CTkButton(row, text="Delete", command=lambda e=expense: self.delete_expense(e[0])).pack(side="right", padx=5)

    def edit_expense(self, expense):
        print(f"Editing Expense: {expense}")

    def delete_expense(self, expense_id):
        delete_expense(expense_id)
        print(f"Deleted Expense ID: {expense_id}")
        self.frame.destroy()
        self.__init__(self.parent)

import wxCharts

class Report(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#D3D3D3")
        self.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self, text="Reports", font=("Poppins", 30, "bold"))
        title.pack(pady=20)

        data = {"Food": 500, "Travel": 1000, "Shopping": 800}
        graph = wxCharts.ScatterChart(self, data)
        graph.pack(expand=True)


class AddExpense(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#D3D3D3")
        self.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self, text="Add Expense", font=("Poppins", 30, "bold"))
        title.pack(pady=20)

        amount_label = ctk.CTkLabel(self, text="Amount", font=("Poppins", 20))
        amount_label.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.pack(pady=5)

        category_label = ctk.CTkLabel(self, text="Category", font=("Poppins", 20))
        category_label.pack(pady=10)

        self.category_entry = ctk.CTkEntry(self)
        self.category_entry.pack(pady=5)

        btn = ctk.CTkButton(self, text="Add Expense", command=self.add_expense)
        btn.pack(pady=20)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        print(f"Expense Added: ₹ {amount} for {category}")


auth = Auth()
auth.signup_screen()

app.mainloop()