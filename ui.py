import customtkinter as ctk
from PIL import Image, ImageTk
from database import add_expense, get_expenses, delete_expense
import sqlite3
from collections import defaultdict

# App Configuration
ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("900x600")
app.title("Expense Tracker")

# Sidebar Toggle Function
def toggle_sidebar():
    if sidebar.winfo_width() == 50:
        sidebar.configure(width=200)
        name_label.pack(pady=10)
        id_label.pack()
    else:
        sidebar.configure(width=50)
        name_label.pack_forget()
        id_label.pack_forget()

# Sidebar
sidebar = ctk.CTkFrame(app, width=50, corner_radius=0, fg_color="#FFD700")
sidebar.pack(side="left", fill="y")

# Toggle Button
menu_icon = ctk.CTkButton(sidebar, text="☰", command=toggle_sidebar)
menu_icon.pack(pady=10)

# Sidebar Content
name_label = ctk.CTkLabel(sidebar, text="Name", font=("Arial", 14))
id_label = ctk.CTkLabel(sidebar, text="ID Number", font=("Arial", 12))

# Main Content Area
main_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
main_frame.pack(side="right", expand=True, fill="both")

# Header
header = ctk.CTkLabel(main_frame, text="Expense Tracker", font=("Arial", 24), text_color="#FFD700")
header.pack(pady=10)

# Navigation Buttons
nav_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
nav_frame.pack(pady=20)

left_frame = ctk.CTkFrame(nav_frame, fg_color="#FFFFFF")
left_frame.grid(row=0, column=0, padx=20)
right_frame = ctk.CTkFrame(nav_frame, fg_color="#FFFFFF")
right_frame.grid(row=0, column=1, padx=20)

ctk.CTkButton(left_frame, text="Dashboard", width=150).pack(pady=10)
ctk.CTkButton(left_frame, text="Analytics", width=150).pack(pady=10)

ctk.CTkButton(right_frame, text="Expenses", width=150).pack(pady=10)
ctk.CTkButton(right_frame, text="Group Budgeting", width=150).pack(pady=10)

app.mainloop()
