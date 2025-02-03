import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import add_expense, get_expenses, delete_expense
import sqlite3
from collections import defaultdict

# App Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.title("Expense Tracker")

# Sidebar Navigation
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Main Content Area
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", expand=True, fill="both")

# Sidebar Buttons
def show_dashboard():
    clear_main_frame()
    ctk.CTkLabel(main_frame, text="Dashboard", font=("Arial", 24)).pack(pady=20)
    # Placeholder for analytics and recent transactions


def show_add_expense():
    clear_main_frame()
    ctk.CTkLabel(main_frame, text="Add Expense", font=("Arial", 24)).pack(pady=20)

    amount_entry = ctk.CTkEntry(main_frame, placeholder_text="Amount")
    amount_entry.pack(pady=5)

    category_entry = ctk.CTkEntry(main_frame, placeholder_text="Category")
    category_entry.pack(pady=5)

    date_entry = ctk.CTkEntry(main_frame, placeholder_text="Date (YYYY-MM-DD)")
    date_entry.pack(pady=5)

    description_entry = ctk.CTkEntry(main_frame, placeholder_text="Description (Optional)")
    description_entry.pack(pady=5)

    def submit_expense():
        add_expense(float(amount_entry.get()), category_entry.get(), date_entry.get(), description_entry.get())
        ctk.CTkLabel(main_frame, text="Expense Added Successfully!", text_color="green").pack()

    ctk.CTkButton(main_frame, text="Add Expense", command=submit_expense).pack(pady=10)


# Analytics Feature

def show_analytics():
    clear_main_frame()
    ctk.CTkLabel(main_frame, text="Analytics", font=("Arial", 24)).pack(pady=20)

    # Pie Chart (Spending by Category)
    expenses = get_expenses()
    category_data = defaultdict(float)

    for expense in expenses:
        category_data[expense[2]] += expense[1]

    fig, ax = plt.subplots()
    ax.pie(category_data.values(), labels=category_data.keys(), autopct='%1.1f%%')
    ax.set_title('Spending by Category')

    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)


# Group Budgeting Feature

def show_group_budgeting():
    clear_main_frame()
    ctk.CTkLabel(main_frame, text="Group Budgeting", font=("Arial", 24)).pack(pady=20)

    group_name_entry = ctk.CTkEntry(main_frame, placeholder_text="Group Name")
    group_name_entry.pack(pady=5)

    members_entry = ctk.CTkEntry(main_frame, placeholder_text="Add Members (comma-separated)")
    members_entry.pack(pady=5)

    def create_group():
        group_name = group_name_entry.get()
        members = members_entry.get().split(",")

        if group_name and members:
            ctk.CTkLabel(main_frame, text=f"Group '{group_name}' Created with Members: {', '.join(members)}", text_color="green").pack(pady=5)

    ctk.CTkButton(main_frame, text="Create Group", command=create_group).pack(pady=10)

    ctk.CTkLabel(main_frame, text="Split Expense", font=("Arial", 18)).pack(pady=10)

    total_amount_entry = ctk.CTkEntry(main_frame, placeholder_text="Total Expense Amount")
    total_amount_entry.pack(pady=5)

    def split_expense():
        total_amount = float(total_amount_entry.get())
        members = members_entry.get().split(",")
        if members and total_amount:
            split_amount = total_amount / len(members)
            result = "\n".join([f"{member.strip()}: {split_amount:.2f}" for member in members])
            ctk.CTkLabel(main_frame, text=f"Split Details:\n{result}", justify="left").pack(pady=5)

    ctk.CTkButton(main_frame, text="Calculate Split", command=split_expense).pack(pady=10)


# Clear Main Frame for Navigation
def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# Sidebar Buttons
ctk.CTkButton(sidebar, text="Dashboard", command=show_dashboard).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Add Expense", command=show_add_expense).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Analytics", command=show_analytics).pack(pady=10, fill="x")
ctk.CTkButton(sidebar, text="Group Budgeting", command=show_group_budgeting).pack(pady=10, fill="x")

# Load Dashboard by Default
show_dashboard()

app.mainloop()
