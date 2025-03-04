import customtkinter as ctk
import sqlite3
import hashlib


class Auth:
    def __init__(self, parent, show_page):
        self.parent = parent
        self.show_page = show_page
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def signup_screen(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.parent, text="Signup", font=("Arial", 24)).pack(pady=20)
        self.username = ctk.CTkEntry(self.parent, placeholder_text="Username")
        self.username.pack(pady=10)
        self.password = ctk.CTkEntry(self.parent, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        ctk.CTkButton(self.parent, text="Signup", command=self.signup).pack(pady=10)
        ctk.CTkButton(self.parent, text="Go to Login", command=self.login_screen).pack(pady=5)

    def login_screen(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.parent, text="Login", font=("Arial", 24)).pack(pady=20)
        self.username = ctk.CTkEntry(self.parent, placeholder_text="Username")
        self.username.pack(pady=10)
        self.password = ctk.CTkEntry(self.parent, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        ctk.CTkButton(self.parent, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self.parent, text="Go to Signup", command=self.signup_screen).pack(pady=5)

    def signup(self):
        username = self.username.get()
        password = self.password.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            print("Signup Successful")
            self.login_screen()
        except sqlite3.IntegrityError:
            print("Username Already Exists")

    def login(self):
        username = self.username.get()
        password = self.password.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            print("Login Successful")
            self.show_page()
        else:
            print("Invalid Credentials")
