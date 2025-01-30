import sqlite3

# Function to create database tables
def create_tables():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        date TEXT NOT NULL,
                        description TEXT
                    )''')
    
    conn.commit()
    conn.close()

# Function to add a new expense
def add_expense(amount, category, date, description=""):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
                   (amount, category, date, description))
    
    conn.commit()
    conn.close()

# Function to fetch all expenses
def get_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    
    conn.close()
    return data

# Function to delete an expense
def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    
    conn.commit()
    conn.close()

# Function to edit an expense
def edit_expense(expense_id, amount, category, date, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE expenses SET amount=?, category=?, date=?, description=? WHERE id=?",
                   (amount, category, date, description, expense_id))
    
    conn.commit()
    conn.close()

# Initialize the database
create_tables()
