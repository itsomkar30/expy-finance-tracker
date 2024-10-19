import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import matplotlib.pyplot as plt
from tkcalendar import DateEntry

from firebase import auth, db


def add_expense(category, amount, description, date, listbox, total_label):
    """Add a new expense."""
    if not current_user_id:
        messagebox.showerror("Error", "Please sign in first.")
        return

    if not category.get() or not amount.get() or not description.get():
        messagebox.showerror("Error", "Please fill in all fields for the expense.")
        return

    try:
        ref = db.child(f'users/{current_user_id}/expenses')
        ref.push({'date': date, 'category': category.get(), 'amount': amount.get(), 'description': description.get()})
        messagebox.showinfo("Success", "Expense recorded successfully")
        # category.delete(0, tk.END)
        category.set("")
        amount.set("")
        description.set("")
        # amount.delete(0, tk.END)
        # description.delete(0, tk.END)
        view_expenses(listbox, total_label)
    except Exception as e:
        messagebox.showerror("Error", f"{e}")


def delete_expense(selected_index, listbox, total_label):
    """Delete an expense based on the selected index."""
    if selected_index is None:
        messagebox.showerror("Error", "Please select an expense to delete.")
        return

    try:
        ref = db.child(f'users/{current_user_id}/expenses')
        # expense_id = listbox.get(selected_index).split(',')[0].split(': ')[1]  # Extracting ID from the listbox entry
        expense_id = idList[selected_index]
        print(selected_index)
        idList.pop(selected_index)
        expenseList.pop(selected_index)
        ref.child(expense_id).remove()  # Remove the expense from Firebase
        messagebox.showinfo("Success", "Expense deleted successfully")
        view_expenses(listbox, total_label)  # Refresh the listbox
    except Exception as e:
        messagebox.showerror("Error", str(e))


def view_expenses(listbox, total_label):
    """View all expenses in the Listbox and show total."""
    if not current_user_id:
        messagebox.showerror("Error", "Please sign in first.")
        return
    global idList, expenseList
    idList = []
    expenseList = []

    ref = db.child(f'users/{current_user_id}/expenses')
    expenses = ref.get()
    total = 0
    listbox.delete(0, tk.END)  # Clear previous list
    if expenses.each():
        for expense in expenses.each():
            expense_data = expense.val()
            print(expense_data)
            expenseList.append(expense_data)
            expense_id = expense.key()
            total = total + int(expense_data['amount'])
            listbox.insert(tk.END,
                           f"Date: {expense_data['date']}, Category: {expense_data['category']}, Amount: {expense_data['amount']}, Description: {expense_data['description']}")
            idList.append(expense_id)
        total_label.config(text=f"Total Expense: ${total:.2f}")
    else:
        listbox.insert(tk.END, "No expenses recorded.")


# def show_pie_chart():
#     """Show a pie chart of expenses by category."""
#     pass
#     if not idList or not expenseList:
#         messagebox.showinfo("No Data", "No expenses to show in pie chart.")
#         return
#
#     categories = {}
#     total = 0
#     for expense in expenseList:
#         date = expense['date']
#         amount = int(expense['amount'])
#         total = total + int(amount)
#         if date in categories:
#             categories[date] += amount
#         else:
#             categories[date] = amount
#
#     labels = categories.keys()
#     sizes = categories.values()
#     print(labels,"==",sizes)
#
#     plt.figure(figsize=(8, 6))
#     plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
#     plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.title(f'Expense Distribution by Date (Total: ${total:.2f})')
#     plt.show()


# new changed pie chart may cause some errors //Omkar

def show_pie_chart():
    """Show a pie chart of expenses by category."""
    if not idList or not expenseList:
        messagebox.showinfo("No Data", "No expenses to show in pie chart.")
        return

    categories = {}
    total = 0

    # Group expenses by category and sum their amounts
    for expense in expenseList:
        category = expense['category']  # Use 'category' instead of 'date'
        amount = int(expense['amount'])
        total += amount
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    labels = categories.keys()  # Set labels to category names
    sizes = categories.values()  # Set sizes to corresponding amounts
    print(labels, "==", sizes)

    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Expense Distribution by Category (Total: ${total:.2f})')
    plt.show()

    # Close the plot to free up resources
    plt.close()

    # categories = {}
    # total = 0


# def switch_theme(root, current_theme):
#     """Switch between dark and light themes."""
#     if current_theme[0] == 'light':
#         theme = 'dark'
#         bg_color = '#2E2E2E'
#         fg_color = '#FFFFFF'
#         btn_bg = '#444444'
#         btn_fg = '#FFFFFF'
#     else:
#         theme = 'light'
#         bg_color = '#FFFFFF'
#         fg_color = '#000000'
#         btn_bg = '#DDDDDD'
#         btn_fg = '#000000'
#
#     root.config(bg=bg_color)
#     for widget in root.winfo_children():
#         widget.config(bg=bg_color, fg=fg_color)
#         if isinstance(widget, tk.Button):
#             widget.config(bg=btn_bg, fg=btn_fg)
#         if isinstance(widget, (tk.Entry, tk.Text)):
#             widget.config(bg=bg_color, fg=fg_color)
#         if isinstance(widget, tk.Listbox):
#             widget.config(bg=bg_color, fg=fg_color, selectbackground=btn_bg, selectforeground=fg_color)
#
#     current_theme[0] = theme


def setup_gui():
    """Setup the GUI components."""
    root = tk.Tk()
    root.title("Expense Tracker")

    expenses = "exp"
    current_theme = ['light']  # Mutable object to store the current theme

    # Create and place widgets
    tk.Label(root, text="Date (DD-MM-YYYY):").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=10)

    category_var = tk.StringVar()
    amount_var = tk.StringVar()
    description_var = tk.StringVar()
    # date_var = str(date.today())

    # tk.Entry(root, textvariable=date_var).grid(row=0, column=1, padx=10, pady=10)
    # tk.Label(root, text=date_var).grid(row=0, column=1, padx=10, pady=10)
    date_entry = DateEntry(root, date_pattern='dd-mm-y')  # Date picker widget
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Entry(root, textvariable=category_var).grid(row=1, column=1, padx=10, pady=10)
    tk.Entry(root, textvariable=amount_var).grid(row=2, column=1, padx=10, pady=10)
    tk.Entry(root, textvariable=description_var).grid(row=3, column=1, padx=10, pady=10)

    tk.Button(root, text="Add Expense",
              command=lambda: add_expense(category_var, amount_var, description_var, str(date_entry.get()),
                                          listbox, total_label)).grid(row=4,
                                                                      column=0,
                                                                      columnspan=2,
                                                                      pady=10)

    listbox = tk.Listbox(root, height=10, width=70)
    listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    total_label = tk.Label(root, text="Total Expense: $0.00")
    total_label.grid(row=6, column=0, columnspan=2)

    tk.Button(root, text="View Expenses", command=lambda: view_expenses(listbox, total_label)).grid(row=7,
                                                                                                    column=0,
                                                                                                    pady=10)

    selected_index = tk.IntVar()

    def on_select(event):
        selected_index.set(listbox.curselection()[0] if listbox.curselection() else None)

    listbox.bind('<<ListboxSelect>>', on_select)

    tk.Button(root, text="Delete Selected Expense",
              command=lambda: delete_expense(selected_index.get(), listbox, total_label)).grid(row=7, column=1, pady=10)

    # Add pie chart button
    tk.Button(root, text="Show Pie Chart", command=lambda: show_pie_chart()).grid(row=8, column=0, columnspan=2,
                                                                                  pady=10)

    # Add theme switch button
    # tk.Button(root, text="Switch Theme", command=lambda: switch_theme(root,current_theme)).grid(row=9, column=0,
    #                                                                                              columnspan=2, pady=10)

    view_expenses(listbox, total_label)  # Initial view
    # switch_theme(root, current_theme)  # Set initial theme

    root.mainloop()


# if __name__ == "__main__":
#     user = auth.sign_in_with_email_and_password("abc@gmail.com", "123456")
#     global current_user_id, id_token, idList
#     idList = []
#     current_user_id = user['localId']
#     id_token = user['idToken']
#     setup_gui()

def main(user):
    global current_user_id, id_token

    current_user_id = user['localId']
    id_token = user['idToken']
    # root = tk.Tk()
    setup_gui()
