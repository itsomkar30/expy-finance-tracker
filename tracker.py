# from firebase import *
# from tkinter import *
# from tkinter import messagebox
# import tkinter as tk
# # from signin import user_uid
#
# root = tk.Tk()
# main_frame = tk.Frame(root)
#
# global user_uid
# def check_user_status(user_uid1):
#     print(f"Current User UID: {user_uid1}")
#     user_uid = user_uid1

#
#
#
# def load_expenses():
#     return "Expenses"
#
#
# def add_expense_gui(expenses, category, amount, description, date, listbox):
#     if not user_uid:
#         messagebox.showerror("Error", "Please sign in first.")
#         return
#
#     if not category or not amount or not date or not description:
#         messagebox.showerror("Error", "Please fill in all fields for the expense.")
#         return
#
#     try:
#         ref = db.child(f'users/{user_uid}/expenses')
#         ref.push({'date': date, 'category': category, 'amount': amount, 'description': description})
#         messagebox.showinfo("Success", "Expense recorded successfully")
#         category_var.delete(0, tk.END)
#         date_var.delete(0, tk.END)
#         amount_var.delete(0, tk.END)
#         description_var.delete(0, tk.END)
#     except Exception as e:
#         messagebox.showerror("Error", f"{e}")
#         print(e)
#
#
# def view_expenses(listbox):
#     if not user_uid:
#         messagebox.showerror("Error", "Please sign in first.")
#         return
#
#     ref = db.child(f'users/{user_uid}/expenses')
#     expenses = ref.get()
#
#     listbox.delete(0, tk.END)  # Clear previous list
#     if expenses.each():
#         for expense in expenses.each():
#             expense_data = expense.val()
#             expense_id = expense.key()
#             listbox.insert(tk.END,
#                            f"ID: {expense_id},Date: {expense_data['date']}, Category: {expense_data['category']}, Amount: {expense_data['amount']}, Description: {expense_data['description']}")
#     else:
#         listbox.insert(tk.END, "No expenses recorded.")
#
#
# def delete_expense(selected_index, listbox):
#     if selected_index is None:
#         messagebox.showerror("Error", "Please select an expense to delete.")
#         return
#
#     try:
#         ref = db.child(f'users/{user_uid}/expenses')
#         expense_id = listbox.get(selected_index).split(',')[0].split(': ')[1]  # Extracting ID from the listbox entry
#         ref.child(expense_id).remove()  # Remove the expense from Firebase
#         messagebox.showinfo("Success", "Expense deleted successfully")
#         view_expenses(listbox)  # Refresh the listbox
#     except Exception as e:
#         messagebox.showerror("Error", str(e))
#         print(e)
#
#
# def switch_theme(current_theme):
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
#
#
# def main_gui():
#     # root = tk.Tk()
#     # root.title("Expense Tracker")
#     # global main_frame
#
#     # main_frame = tk.Frame(root)
#     expenses = load_expenses()
#     current_theme = ['light']  # Mutable object to store the current theme
#
#     # Create and place widgets
#     tk.Label(main_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
#     tk.Label(main_frame, text="Category:").grid(row=1, column=0, padx=10, pady=10)
#     tk.Label(main_frame, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
#     tk.Label(main_frame, text="Description:").grid(row=3, column=0, padx=10, pady=10)
#
#     global category_var, amount_var, description_var, date_var
#     category_var = tk.Entry(main_frame)
#     category_var.grid(row=1, column=1, padx=10, pady=10)
#     amount_var = tk.Entry(main_frame)
#     amount_var.grid(row=2, column=1, padx=10, pady=10)
#     description_var = tk.Entry(main_frame)
#     description_var.grid(row=3, column=1, padx=10, pady=10)
#     date_var = tk.Entry(main_frame)
#     date_var.grid(row=0, column=1, padx=10, pady=10)
#
#     tk.Button(main_frame, text="Add Expense",
#               command=lambda: add_expense_gui(expenses, category_var.get(), amount_var.get(), description_var.get(),
#                                               date_var.get(), listbox)).grid(row=4, column=0, columnspan=2, pady=10)
#
#     listbox = tk.Listbox(main_frame, height=10, width=70)
#     listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
#
#     tk.Button(main_frame, text="View Expenses", command=lambda: view_expenses(listbox)).grid(row=6, column=0,
#                                                                                              pady=10)
#
#     selected_index = tk.IntVar()
#
#     def on_select(event):
#         selected_index.set(listbox.curselection()[0] if listbox.curselection() else None)
#
#     listbox.bind('<<ListboxSelect>>', on_select)
#
#     tk.Button(main_frame, text="Delete Selected Expense",
#               command=lambda: delete_expense(selected_index.get(), listbox)).grid(row=6, column=1, pady=10)
#
#     # Add theme switch button
#     # tk.Button(main_frame, text="Switch Theme", command=lambda: switch_theme(current_theme)).grid(row=7, column=0, pady=10, padx=10)


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
        view_expenses(listbox,total_label)
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

def show_pie_chart():
    """Show a pie chart of expenses by category."""
    pass
    if not idList or not expenseList:
        messagebox.showinfo("No Data", "No expenses to show in pie chart.")
        return

    categories = {}
    total = 0
    for expense in expenseList:
        date = expense['date']
        amount = int(expense['amount'])
        total = total + int(amount)
        if date in categories:
            categories[date] += amount
        else:
            categories[date] = amount

    labels = categories.keys()
    sizes = categories.values()
    print(labels,"==",sizes)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Expense Distribution by Date (Total: ${total:.2f})')
    plt.show()
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
    global current_user_id, id_token, idList ,expenseList
    idList = []
    expenseList = []
    current_user_id = user['localId']
    id_token = user['idToken']
    # root = tk.Tk()
    setup_gui()
