import customtkinter as ctk
from datetime import datetime
from db.database import add_expense, get_expenses


class ExpensePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="Add Expense", font=("Arial", 24)).pack(pady=20)
        self.expense_name = ctk.CTkEntry(self, placeholder_text="Description")
        self.expense_name.pack(pady=10)

        self.amount = ctk.CTkEntry(self, placeholder_text="Amount")
        self.amount.pack(pady=10)

        self.category = ctk.CTkEntry(self, placeholder_text="Category")
        self.category.pack(pady=10)

        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.pack(pady=10)

        ctk.CTkButton(self, text="Add Expense", command=self.add_expense).pack(pady=10)

        self.expense_list_frame = ctk.CTkFrame(self)
        self.expense_list_frame.pack(pady=20, fill="both", expand=True)

        self.show_expenses()

    def add_expense(self):
        name = self.expense_name.get()
        amt = self.amount.get()
        category = self.category.get()
        date = datetime.now().strftime("%Y-%m-%d")

        if name and amt and category:
            try:
                add_expense(float(amt), category, date, name)
                self.message_label.configure(text="Expense Added ✅", fg_color="green")
                self.show_expenses()  # Refresh List
            except Exception as e:
                self.message_label.configure(text=f"Database Error ❌ {e}", fg_color="red")
        else:
            self.message_label.configure(text="Please Fill All Fields ❌", fg_color="red")

        self.after(2000, lambda: self.message_label.configure(text="", fg_color="transparent"))

    def show_expenses(self):
        for widget in self.expense_list_frame.winfo_children():
            widget.destroy()

        expenses = get_expenses()
        for expense in expenses:
            expense_text = f"{expense[1]} Rs - {expense[2]} - {expense[3]}"
            ctk.CTkLabel(self.expense_list_frame, text=expense_text).pack(pady=5)
