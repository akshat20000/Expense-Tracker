import customtkinter as ctk
from PIL import Image
from database import add_expense, get_expenses, delete_expense, edit_expense
import sqlite3
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib

# App Configuration
ctk.set_appearance_mode("light")

class WalletApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Wallet App - Expense Tracker & Budget Manager")
        self.auth = Auth()
        self.logged_in = False
        self.init_ui()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def init_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=0, height=600)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar_visible = False

        self.btn_toggle = ctk.CTkButton(self, text="Toggle Sidebar", command=self.toggle_sidebar)
        self.btn_toggle.pack(pady=10)

        self.btn_report = ctk.CTkButton(self, text="Generate Report", command=self.generate_report)
        self.btn_report.pack(pady=10)

        self.btn_backup = ctk.CTkButton(self, text="Backup Data", command=self.backup_data)
        self.btn_backup.pack(pady=10)

        self.btn_restore = ctk.CTkButton(self, text="Restore Data", command=self.restore_data)
        self.btn_restore.pack(pady=10)

        self.login_frame()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_visible = True

    def login_frame(self):
        self.login_window = ctk.CTkFrame(self)
        self.login_window.pack(pady=100)

        self.username_entry = ctk.CTkEntry(self.login_window, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.login_window, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        self.login_btn = ctk.CTkButton(self.login_window, text="Login", command=self.login)
        self.login_btn.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth.login(username, password):
            self.login_window.pack_forget()
            print("Login Successful")
        else:
            print("Invalid Credentials")

    def generate_report(self):
        expenses = get_expenses()
        categories = defaultdict(float)
        for expense in expenses:
            categories[expense[2]] += float(expense[1])
        fig, ax = plt.subplots()
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def backup_data(self):
        import shutil
        shutil.copy("expenses.db", "backup.db")
        print("Backup Created!")

    def restore_data(self):
        import shutil
        shutil.copy("backup.db", "expenses.db")
        print("Data Restored!")

class Auth:
    def __init__(self):
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()
        self.create_users_table()

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
            print(f"User {username} registered successfully!")
        except sqlite3.IntegrityError:
            print("Username already exists!")

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False

if __name__ == "__main__":
    app = WalletApp()
    app.mainloop()
