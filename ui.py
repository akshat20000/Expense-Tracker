import customtkinter as ctk
from PIL import Image, ImageTk
from database import add_expense, get_expenses, delete_expense
import sqlite3
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# App Configuration
ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("900x600")
app.title("Expense Tracker")

# Sidebar Toggle Function with Smooth Transition
def toggle_sidebar():
    current_width = sidebar.winfo_width()
    target_width = 200 if current_width == 0 else 0
    step = 5 if current_width < target_width else -5
    duration = 2000  # 2 seconds
    delay = abs(duration // ((target_width - current_width) // step if step != 0 else 1))

    def animate():
        nonlocal current_width
        if (step > 0 and current_width < target_width) or (step < 0 and current_width > target_width):
            current_width += step
            sidebar.configure(width=current_width)
            app.after(delay, animate)

    animate()

# Hide sidebar initially
sidebar = ctk.CTkFrame(app, width=0, corner_radius=0, fg_color="#FFD700")
sidebar.pack(side="left", fill="y")

# Sidebar Content
name_label = ctk.CTkLabel(sidebar, text="Name", font=("Arial", 14))
id_label = ctk.CTkLabel(sidebar, text="ID Number", font=("Arial", 12))
name_label.pack(pady=10)
id_label.pack()

# Main Content Area
main_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
main_frame.pack(side="right", expand=True, fill="both")

# Header
header = ctk.CTkLabel(main_frame, text="Expense Tracker", font=("Arial", 24), text_color="#FFD700")
header.pack(pady=10)

# Three-line Menu Button
menu_icon = ctk.CTkButton(main_frame, text="☰", text_color="#FFD700", width=30, command=toggle_sidebar)
menu_icon.place(x=10, y=10)

# Click to Hide Sidebar
app.bind("<Button-1>", lambda event: toggle_sidebar() if sidebar.winfo_width() > 0 and not sidebar.winfo_containing(event.x_root, event.y_root) else None)

# Navigation Buttons
nav_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF")
nav_frame.pack(pady=20)

left_frame = ctk.CTkFrame(nav_frame, fg_color="#FFFFFF")
left_frame.grid(row=0, column=0, padx=20)
right_frame = ctk.CTkFrame(nav_frame, fg_color="#FFFFFF")
right_frame.grid(row=0, column=1, padx=20)

ctk.CTkButton(left_frame, text="Dashboard", width=150, command=lambda: show_content("dashboard")).pack(pady=10)
ctk.CTkButton(left_frame, text="Analytics", width=150, command=lambda: show_content("analytics")).pack(pady=10)

ctk.CTkButton(right_frame, text="Expenses", width=150, command=lambda: show_content("expenses")).pack(pady=10)
ctk.CTkButton(right_frame, text="Group Budgeting", width=150, command=lambda: show_content("group_budgeting")).pack(pady=10)

# Content Display Function
def show_content(section):
    for widget in main_frame.winfo_children():
        if widget not in [header, nav_frame, menu_icon]:
            widget.destroy()

    if section == "dashboard":
        ctk.CTkLabel(main_frame, text="Dashboard Content", font=("Arial", 16)).pack(pady=10)

    elif section == "analytics":
        analytics_label = ctk.CTkLabel(main_frame, text="Analytics", font=("Arial", 16))
        analytics_label.pack(pady=10)

        expenses = get_expenses()
        total_expense = sum(exp[0] for exp in expenses)
        ctk.CTkLabel(main_frame, text=f"Total Expenses: {total_expense}").pack()

        # Bar Graph
        categories = defaultdict(int)
        for expense in expenses:
            amount, category = expense[0], expense[1]  # Safely unpack the first two values
            categories[category] += int(amount)

        fig, ax = plt.subplots()
        ax.bar(categories.keys(), categories.values(), color="#FFD700")
        ax.set_title("Expenses by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")

        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    elif section == "expenses":
        expense_frame = ctk.CTkFrame(main_frame)
        expense_frame.pack(pady=10)

        amount_entry = ctk.CTkEntry(expense_frame, placeholder_text="Amount")
        amount_entry.pack(side="left", padx=5)

        category_entry = ctk.CTkEntry(expense_frame, placeholder_text="Category")
        category_entry.pack(side="left", padx=5)

        date_entry = ctk.CTkEntry(expense_frame, placeholder_text="Date (YYYY-MM-DD)")
        date_entry.pack(side="left", padx=5)

        def add_new_expense():
            add_expense(amount_entry.get(), category_entry.get(), date_entry.get())
            show_content("expenses")

        ctk.CTkButton(expense_frame, text="Add Expense", command=add_new_expense).pack(side="left", padx=5)

        expenses = get_expenses()
        for expense in expenses:
            expense_label = ctk.CTkLabel(main_frame, text=f"Amount: {expense[0]}, Category: {expense[1]}, Date: {expense[2]}")
            expense_label.pack()

    elif section == "group_budgeting":
        ctk.CTkLabel(main_frame, text="Group Budgeting Content", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(main_frame, text="Feature under development").pack()

app.mainloop()
