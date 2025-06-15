import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import pickle
import os
from collections import defaultdict
import matplotlib.pyplot as plt

expenses = []
selected_item = None  # For editing

def add_or_update_expense():
    global selected_item
    date = date_entry.get() or datetime.date.today().isoformat()
    time = time_entry.get() or datetime.datetime.now().strftime("%H:%M")
    category = category_entry.get()
    note = note_entry.get()
    
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid amount.")
        return

    if selected_item:
        index = int(expense_list.item(selected_item, 'values')[0]) - 1
        expenses[index].update({"date": date, "time": time, "category": category, "amount": amount, "note": note})
        selected_item = None
        add_button.config(text="Add Expense")
    else:
        expenses.append({"date": date, "time": time, "category": category, "amount": amount, "note": note})
    
    save_expenses()
    update_expense_list()
    update_total()
    clear_inputs()

def delete_expense():
    global selected_item
    if not selected_item:
        messagebox.showinfo("Select", "Please select a row to delete.")
        return
    index = int(expense_list.item(selected_item, 'values')[0]) - 1
    del expenses[index]
    selected_item = None
    save_expenses()
    update_expense_list()
    update_total()
    clear_inputs()
    add_button.config(text="Add Expense")

def select_expense(event):
    global selected_item
    selected_item = expense_list.focus()
    if not selected_item:
        return
    values = expense_list.item(selected_item, 'values')
    if values:
        index = int(values[0]) - 1
        exp = expenses[index]
        date_entry.delete(0, tk.END)
        date_entry.insert(0, exp['date'])
        time_entry.delete(0, tk.END)
        time_entry.insert(0, exp['time'])
        category_entry.delete(0, tk.END)
        category_entry.insert(0, exp['category'])
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, str(exp['amount']))
        note_entry.delete(0, tk.END)
        note_entry.insert(0, exp['note'])
        add_button.config(text="Update Expense")

def clear_inputs():
    global selected_item
    for entry in [date_entry, time_entry, category_entry, amount_entry, note_entry]:
        entry.delete(0, tk.END)
    selected_item = None
    add_button.config(text="Add Expense")

def update_expense_list(filtered=None):
    expense_list.delete(*expense_list.get_children())
    display = filtered if filtered else expenses
    for i, exp in enumerate(display, 1):
        expense_list.insert('', 'end', values=(i, exp['date'], exp['time'], exp['category'], f"₹{exp['amount']}", exp['note']))

def update_total():
    total = sum(exp['amount'] for exp in expenses)
    total_label.config(text=f"Total Spent: ₹{total}")

def filter_expenses():
    cat = filter_category.get().strip().lower()
    date = filter_date.get().strip()
    filtered = [
        exp for exp in expenses
        if (not cat or cat in exp['category'].lower()) and (not date or date == exp['date'])
    ]
    update_expense_list(filtered)

def show_chart():
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp['category']] += exp['amount']
    if not category_totals:
        messagebox.showinfo("No Data", "No data to show in chart.")
        return
    plt.figure(figsize=(8, 5))
    plt.bar(category_totals.keys(), category_totals.values(), color='orange')
    plt.xlabel('Category')
    plt.ylabel('Total ₹ Spent')
    plt.title('Expenses by Category')
    plt.tight_layout()
    plt.show()

def save_expenses():
    with open("expenses.pkl", "wb") as f:
        pickle.dump(expenses, f)

def load_expenses():
    global expenses
    if os.path.exists("expenses.pkl"):
        with open("expenses.pkl", "rb") as f:
            expenses = pickle.load(f)

def fade_in(window, alpha=0.0):
    if alpha < 1.0:
        alpha += 0.05
        window.attributes("-alpha", alpha)
        window.after(30, lambda: fade_in(window, alpha))

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("💸 Expense Tracker - Dark Mode")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e", rowheight=25)
style.configure("Treeview.Heading", background="#444", foreground="white", font=('Arial', 10, 'bold'))
style.map('Treeview', background=[('selected', '#007acc')])

input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(padx=10, pady=10, fill='x')

def dark_label(text, row, col):
    lbl = tk.Label(input_frame, text=text, fg="white", bg="#1e1e1e")
    lbl.grid(row=row, column=col, sticky='w')
    return lbl

dark_label("Date:", 0, 0)
date_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1)

dark_label("Time (HH:MM):", 0, 2)
time_entry = tk.Entry(input_frame)
time_entry.grid(row=0, column=3)

dark_label("Category:", 1, 0)
category_entry = tk.Entry(input_frame)
category_entry.grid(row=1, column=1)

dark_label("Amount ₹:", 1, 2)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=1, column=3)

dark_label("Note:", 2, 0)
note_entry = tk.Entry(input_frame, width=50)
note_entry.grid(row=2, column=1, columnspan=3)

add_button = tk.Button(input_frame, text="Add Expense", command=add_or_update_expense, bg="#28a745", fg="white")
add_button.grid(row=3, column=0, columnspan=2, pady=10)

delete_button = tk.Button(input_frame, text="Delete Selected", command=delete_expense, bg="#dc3545", fg="white")
delete_button.grid(row=3, column=2, columnspan=2)

# Filter Section
dark_label("Filter by Category:", 4, 0)
filter_category = tk.Entry(input_frame)
filter_category.grid(row=4, column=1)

dark_label("Filter by Date:", 4, 2)
filter_date = tk.Entry(input_frame)
filter_date.grid(row=4, column=3)

filter_button = tk.Button(input_frame, text="🔍 Filter", command=filter_expenses, bg="#007bff", fg="white")
filter_button.grid(row=5, column=0, columnspan=4, pady=5)

# Expense List
columns = ('#', 'Date', 'Time', 'Category', 'Amount', 'Note')
expense_list = ttk.Treeview(root, columns=columns, show='headings', height=12)
for col in columns:
    expense_list.heading(col, text=col)
    expense_list.column(col, width=120)
expense_list.bind("<<TreeviewSelect>>", select_expense)
expense_list.pack(fill='both', padx=10, pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient='vertical', command=expense_list.yview)
expense_list.configure(yscroll=scrollbar.set)
scrollbar.place(relx=0.975, rely=0.37, relheight=0.51)

total_label = tk.Label(root, text="Total Spent: ₹0", font=('Arial', 14, 'bold'), fg="white", bg="#1e1e1e")
total_label.pack(pady=5)

chart_button = tk.Button(root, text="📊 Show Category Chart", command=show_chart, bg="#ffc107")
chart_button.pack(pady=5)

load_expenses()
update_expense_list()
update_total()

# Apply Fade-In Animation on App Load
root.attributes("-alpha", 0.0)
fade_in(root)

root.mainloop()
