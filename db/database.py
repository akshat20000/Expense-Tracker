import sqlite3


def create_tables():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_expense(amount, category, date, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)', (amount, category, date, description))
    conn.commit()
    conn.close()
def get_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    conn.close()
    return data


create_tables()
