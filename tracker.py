import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tkcalendar import DateEntry
from firebase import auth, db
import json

DATA_FILE = 'logged_user.json'


# def add_expense(category, amount, description, date, listbox, total_label):
#     """Add a new expense."""
#     if not current_user_id:
#         messagebox.showerror("Error", "Please sign in first.")
#         return
#
#     if not category.get() or not amount.get() or not description.get():
#         messagebox.showerror("Error", "Please fill in all fields for the expense.")
#         return
#
#     try:
#         ref = db.child(f'users/{current_user_id}/expenses')
#         ref.push({'date': date, 'category': category.get(), 'amount': amount.get(), 'description': description.get()})
#         messagebox.showinfo("Success", "Expense recorded successfully")
#         # category.delete(0, tk.END)
#         category.set("")
#         amount.set("")
#         description.set("")
#         # amount.delete(0, tk.END)
#         # description.delete(0, tk.END)
#         view_expenses(listbox, total_label)
#     except Exception as e:
#         messagebox.showerror("Error", f"{e}")


def add_expense(category, amount, description, date, listbox, total_label):
    """Add a new expense with date, month, and year stored as integers."""
    if not current_user_id:
        messagebox.showerror("Error", "Please sign in first.")
        return

    if not category.get() or not amount.get() or not description.get():
        messagebox.showerror("Error", "Please fill in all fields for the expense.")
        return

    try:
        # Split the date into day, month, and year and convert them to integers
        day, month, year = map(int, date.split("-"))

        ref = db.child(f'users/{current_user_id}/expenses')
        # Store day, month, and year as integers along with the full date
        ref.push({
            'date': date,
            'day': day,  # Integer format
            'month': month,  # Integer format
            'year': year,  # Integer format
            'category': category.get(),
            'amount': amount.get(),
            'description': description.get()
        })
        messagebox.showinfo("Success", "Expense recorded successfully")

        # Clear input fields
        category.set("")
        amount.set("")
        description.set("")

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


def show_pie_chart_date(idList, expenseList):
    """Show a pie chart of expenses by category."""
    if not idList or not expenseList:
        messagebox.showinfo("No Data", "No expenses to show in pie chart.")
        return

    categories = {}
    total = 0

    # Group expenses by category and sum their amounts
    for expense in expenseList:
        category = expense['date']  # Use 'category' instead of 'date'
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


def show_pie_chart_transaction_type():
    """Show a pie chart of expenses by category."""
    if not idList or not expenseList:
        messagebox.showinfo("No Data", "No expenses to show in pie chart.")
        return

    categories = {}
    total = 0

    # Group expenses by category and sum their amounts
    for expense in expenseList:
        category = expense['description']  # Use 'category' instead of 'date'
        amount = int(expense['amount'])
        total += amount
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    labels = categories.keys()  # Set labels to category names
    sizes = categories.values()  # Set sizes to corresponding amounts
    print(labels, "==", sizes)

    def autopct_label(pct):
        amount = pct * total / 100
        return f'{pct:.1f}%\n(${amount:.2f})'

    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    # plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.pie(sizes, labels=labels, autopct=autopct_label, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Expense Distribution by Category (Total: ${total:.2f})')
    plt.show()

    # Close the plot to free up resources
    plt.close()


# categories = {}
# total = 0


def show_bar_by_month(idList, expenseList):
    """Show a bar chart of expenses by date with different colors for each bar."""
    if not idList or not expenseList:
        messagebox.showinfo("No Data", "No expenses to show in the bar chart.")
        return

    categories = {}
    total = 0

    # Process each expense
    for expense in expenseList:
        date = expense['date']
        month = date[3:5]  # Extract the month (assuming date is in DDMMYYYY format)
        amount = int(expense['amount'])
        total += amount

        # Accumulate expenses by month
        if month in categories:
            categories[month] += amount
        else:
            categories[month] = amount

    labels = list(categories.keys())
    values = list(categories.values())

    # Generate distinct colors for each bar
    num_bars = len(labels)
    colors = cm.get_cmap('tab20', num_bars).colors  # Use a colormap with 'num_bars' different colors

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors)  # Use different colors for each bar
    plt.xlabel('Month')
    plt.ylabel('Expense Amount ($)')
    plt.title(f'Expense Distribution by Month (Total: ${total:.2f})')
    plt.xticks(rotation=45, ha='right')  # Rotate month labels for readability
    plt.tight_layout()  # Adjust layout to prevent label clipping

    for bar in bars:
        yval = bar.get_height()  # Get the height of the bar (value)
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval}',
                 ha='center', va='bottom', fontsize=10)  # Centered text above the bar

    plt.show()

    # Close the figure to prevent memory issues
    plt.close()


def get_name():
    try:
        data = db.child(f'users/{current_user_id}/username').get()
        return data.val()
    except Exception as e:
        return e


def log_out(root, tabs):
    expenses = []
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

    for tab in tabs:
        tab.destroy()

    # Destroy the root window
    root.destroy()


def tabControls(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    # Customize the style for tabs
    style.configure(
        'TNotebook.Tab',
        font=('Helvetica', 12, 'bold'),
        padding=[10, 5],  # Fixed padding
        width=15,  # Fixed width to prevent size change
        focuscolor="",  # Remove focus outline
        highlightthickness=0  # Remove border outline
    )

    # Prevent the background color change from affecting the tab size
    style.map(
        'TNotebook.Tab',
        background=[('selected', '#4CAF50'), ('!selected', '#E0E0E0')],
        padding=[('selected', [10, 5])]  # Keep the padding consistent
    )

    # Customize the style for labels
    style.configure('TLabel', font=('Helvetica', 14), padding=10)

    # Create a notebook (tab container)
    tab_control = ttk.Notebook(root)

    # Create different tabs
    tab1 = ttk.Frame(tab_control, padding=20)
    tab2 = ttk.Frame(tab_control, padding=20)
    tab3 = ttk.Frame(tab_control, padding=20)

    # Add tabs to the notebook
    tab_control.add(tab1, text="Home")
    tab_control.add(tab2, text="Charts")
    tab_control.add(tab3, text="About")

    # Display the notebook
    tab_control.pack(expand=1, fill='both')
    return [tab1, tab2, tab3]


def charts(tab):
    try:
        original_image = Image.open('assets/charts.jpeg')  # Replace with your image path
        resized_image = original_image.resize((450, 250), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading image: {e}")
        image = None

    # Add the image above the "Show Pie Chart By Categories" button
    if image:
        tk.Label(tab, image=image).grid(row=1, column=0, columnspan=2, pady=10)  # Place image at row 1
        tab.image = image  # Keep a reference to the image to prevent garbage collection

    tk.Button(tab, text="Show Pie Chart By Categories", command=lambda: show_pie_chart()).grid(
        row=2, column=0, columnspan=2, pady=10, sticky='ew'
    )

    tk.Button(tab, text="Show Pie Chart By Date", command=lambda: show_pie_chart_date(idList, expenseList)).grid(
        row=4, column=0, columnspan=2, pady=10, sticky='ew'
    )

    tk.Button(tab, text="Show Bar Chart By Month", command=lambda: show_bar_by_month(idList, expenseList)).grid(
        row=6, column=0, columnspan=2, pady=10, sticky='ew'
    )

    tk.Button(tab, text="Show Bar Chart By Transaction Type",
              command=lambda: show_pie_chart_transaction_type()).grid(
        row=7, column=0, columnspan=2, pady=10, sticky='ew'
    )
    # Configure the grid columns to expand equally
    tab.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
    tab.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand


def about(tab, root, tabs):
    try:
        original_image = Image.open('assets/user.png')  # Replace with your image path
        resized_image = original_image.resize((40, 40), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading image: {e}")
        image = None

    # Add the image above the "Show Pie Chart By Categories" button
    if image:
        tk.Label(tab, image=image).grid(row=1, column=0, sticky='w', padx=20, pady=10)  # Align left with 30px padding
        tab.image = image  # Keep a reference to the image to prevent garbage collection

    tk.Label(tab, text=f"Hello, {get_name()} !", font=("Helvetica", 14)).grid(
        row=1, column=0, padx=(60, 0), pady=(0, 10)  # Label next to image, with padding
    )

    tk.Button(tab, text="Log out", command=lambda: log_out(root, tabs),
              font=("Helvetica", 10), height=2).grid(
        row=4, column=0, columnspan=2, pady=10, sticky='ew'
    )

    # Configure the grid columns to expand equally
    tab.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
    tab.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand


def setup_gui():
    """Set up the GUI components."""
    root = tk.Tk()
    root.title("Expense Tracker")

    tab = tabControls(root)
    charts(tab[1])
    about(tab[2], root, tab)
    print(get_name())
    name = get_name()

    expenses = "exp"
    current_theme = ['light']  # Mutable object to store the current theme

    # Create and place widgets
    # tk.Label(tab[0], text="Hello, " + name + " !").place(x=0, y=0)
    tk.Label(tab[0], text="Date (DD-MM-YYYY):").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(tab[0], text="Category:").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(tab[0], text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(tab[0], text="Payment Type:").grid(row=3, column=0, padx=10, pady=10)

    category_var = tk.StringVar()
    amount_var = tk.StringVar()
    description_var = tk.StringVar()
    # date_var = str(date.today())

    # tk.Entry(root, textvariable=date_var).grid(row=0, column=1, padx=10, pady=10)
    # tk.Label(root, text=date_var).grid(row=0, column=1, padx=10, pady=10)
    date_entry = DateEntry(tab[0], date_pattern='dd-mm-y')  # Date picker widget
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Entry(tab[0], textvariable=category_var).grid(row=1, column=1, padx=10, pady=10)
    tk.Entry(tab[0], textvariable=amount_var).grid(row=2, column=1, padx=10, pady=10)
    # tk.Entry(tab[0], textvariable=description_var).grid(row=3, column=1, padx=10, pady=10)

    radio_frame = tk.Frame(tab[0])
    radio_frame.grid(row=3, column=1, padx=40, pady=10, sticky="w")

    # Radio button for "Cash"
    tk.Radiobutton(radio_frame, text="Cash", variable=description_var, value="cash").pack(side="left", padx=(0, 10))

    # Radio button for "Online"
    tk.Radiobutton(radio_frame, text="Online", variable=description_var, value="online").pack(side="left")

    # Radio button for "Online"
    tk.Radiobutton(radio_frame, text="Cheque", variable=description_var, value="cheque").pack(side="left")

    # Set a default value (if you want, e.g., default to "Cash")
    description_var.set("Cash")

    tk.Button(tab[0], text="Add Expense",
              command=lambda: add_expense(category_var, amount_var, description_var, str(date_entry.get()),
                                          listbox, total_label)).grid(row=4,
                                                                      column=0,
                                                                      columnspan=2,
                                                                      pady=10)

    listbox = tk.Listbox(tab[0], height=10, width=70)
    listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    total_label = tk.Label(tab[0], text="Total Expense: $0.00")
    total_label.grid(row=6, column=0, columnspan=2)

    tk.Button(tab[0], text="View Expenses", command=lambda: view_expenses(listbox, total_label)).grid(row=7,
                                                                                                      column=0,
                                                                                                      pady=10)

    selected_index = tk.IntVar()

    def on_select(event):
        selected_index.set(listbox.curselection()[0] if listbox.curselection() else None)

    listbox.bind('<<ListboxSelect>>', on_select)

    tk.Button(tab[0], text="Delete Selected Expense",
              command=lambda: delete_expense(selected_index.get(), listbox, total_label)).grid(row=7, column=1, pady=10)

    # tk.Button(root, text="Show Pie Chart By Month", command=lambda: show_pie_chart_month()).grid(row=10, column=0,
    #                                                                                            columnspan=2,
    #                                                                                            pady=10)

    # Add theme switch button
    # tk.Button(root, text="Switch Theme", command=lambda: switch_theme(root,current_theme)).grid(row=9, column=0,
    #                                                                                              columnspan=2, pady=10)

    view_expenses(listbox, total_label)  # Initial view
    # switch_theme(root, current_theme)  # Set initial theme

    root.mainloop()


def main(user):
    global current_user_id, id_token

    current_user_id = user['localId']
    id_token = user['idToken']
    # root = tk.Tk()
    setup_gui()
