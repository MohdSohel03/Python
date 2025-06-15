import tkinter as tk
from ttkbootstrap import Toplevel, Label, Entry, Button, Frame, Combobox
from database import get_connection
from ttkbootstrap.constants import *
from datetime import datetime

def open_transaction_window(root):
    win = Toplevel(root)
    win.title("Record Transaction")
    win.geometry("600x400")

    frame = Frame(win, padding=10)
    frame.pack(fill="both", expand=True)

    Label(frame, text="Transaction Type").grid(row=0, column=0)
    type_box = Combobox(frame, values=["purchase", "sale"])
    type_box.grid(row=0, column=1)

    Label(frame, text="Product ID").grid(row=1, column=0)
    pid_entry = Entry(frame)
    pid_entry.grid(row=1, column=1)

    Label(frame, text="Quantity").grid(row=2, column=0)
    qty_entry = Entry(frame)
    qty_entry.grid(row=2, column=1)

    def save_transaction():
        conn = get_connection()
        cursor = conn.cursor()
        trans_type = type_box.get()
        pid = int(pid_entry.get())
        qty = int(qty_entry.get())
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("SELECT cost_price, sell_price, quantity FROM products WHERE id = ?", (pid,))
        product = cursor.fetchone()
        if not product:
            win.destroy()
            return

        cost, sell, current_qty = product
        total = qty * (cost if trans_type == "purchase" else sell)

        if trans_type == "sale" and qty > current_qty:
            win.destroy()
            return

        new_qty = current_qty + qty if trans_type == "purchase" else current_qty - qty
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, pid))
        cursor.execute("INSERT INTO transactions (type, date, product_id, quantity, total) VALUES (?, ?, ?, ?, ?)",
                       (trans_type, date, pid, qty, total))

        conn.commit()
        conn.close()
        win.destroy()

    Button(frame, text="Save Transaction", command=save_transaction, bootstyle=SUCCESS).grid(row=3, column=1, pady=10)
