import customtkinter as ctk
from database import add_expense, get_expenses, delete_expense

# Function to add an expense
def submit_expense():
    amount = entry_amount.get()
    category = entry_category.get()
    date = entry_date.get()
    description = entry_description.get()
    
    if amount and category and date:
        add_expense(float(amount), category, date, description)
        label_status.configure(text="Expense Added!", fg_color="green")
        refresh_expenses()
    else:
        label_status.configure(text="Please fill all fields!", fg_color="red")

# Function to delete an expense
def remove_expense():
    selected_id = entry_delete.get()  # Get ID from user input
    if selected_id.isdigit():
        delete_expense(int(selected_id))
        refresh_expenses()
        label_status.configure(text="Expense Deleted!", fg_color="green")
    else:
        label_status.configure(text="Enter a valid expense ID!", fg_color="red")

# Function to refresh the expense list
def refresh_expenses():
    for widget in expense_list_frame.winfo_children():
        widget.destroy()  # Clear previous items
    
    expenses = get_expenses()
    for expense in expenses:
        label = ctk.CTkLabel(expense_list_frame, text=f"{expense[0]} - {expense[1]} USD | {expense[2]} | {expense[3]}")
        label.pack(anchor="w", padx=10, pady=2)

# UI Setup
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("500x600")
app.title("Expense Tracker")

label_title = ctk.CTkLabel(app, text="Add Expense", font=("Arial", 20))
label_title.pack(pady=10)

entry_amount = ctk.CTkEntry(app, placeholder_text="Amount")
entry_amount.pack(pady=5)

entry_category = ctk.CTkEntry(app, placeholder_text="Category")
entry_category.pack(pady=5)

entry_date = ctk.CTkEntry(app, placeholder_text="Date (YYYY-MM-DD)")
entry_date.pack(pady=5)

entry_description = ctk.CTkEntry(app, placeholder_text="Description (Optional)")
entry_description.pack(pady=5)

button_submit = ctk.CTkButton(app, text="Add Expense", command=submit_expense)
button_submit.pack(pady=10)

label_status = ctk.CTkLabel(app, text="")
label_status.pack(pady=5)

# Expense List Frame
expense_list_frame = ctk.CTkScrollableFrame(app, width=400, height=200)
expense_list_frame.pack(pady=10, expand=True, fill="both")

# Delete Expense Section
label_delete = ctk.CTkLabel(app, text="Enter ID to Delete:")
label_delete.pack(pady=5)
entry_delete = ctk.CTkEntry(app, placeholder_text="Expense ID")
entry_delete.pack(pady=5)

button_delete = ctk.CTkButton(app, text="Delete Expense", command=remove_expense)
button_delete.pack(pady=5)

refresh_expenses()  # Load existing expenses

app.mainloop()
