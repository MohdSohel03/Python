import tkinter as tk
from ttkbootstrap import Toplevel, Label, Entry, Button, Frame, Style
from database import get_connection
from ttkbootstrap.constants import *

def open_product_window(root):
    win = Toplevel(root)
    win.title("Product Manager")
    win.geometry("600x400")

    frame = Frame(win, padding=10)
    frame.pack(fill="both", expand=True)

    Label(frame, text="Product Name").grid(row=0, column=0)
    name_entry = Entry(frame)
    name_entry.grid(row=0, column=1)

    Label(frame, text="SKU").grid(row=1, column=0)
    sku_entry = Entry(frame)
    sku_entry.grid(row=1, column=1)

    Label(frame, text="Quantity").grid(row=2, column=0)
    qty_entry = Entry(frame)
    qty_entry.grid(row=2, column=1)

    Label(frame, text="Cost Price").grid(row=3, column=0)
    cost_entry = Entry(frame)
    cost_entry.grid(row=3, column=1)

    Label(frame, text="Sell Price").grid(row=4, column=0)
    sell_entry = Entry(frame)
    sell_entry.grid(row=4, column=1)

    def save_product():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products(name, sku, quantity, cost_price, sell_price) VALUES (?, ?, ?, ?, ?)",
                       (name_entry.get(), sku_entry.get(), qty_entry.get(), cost_entry.get(), sell_entry.get()))
        conn.commit()
        conn.close()
        win.destroy()

    Button(frame, text="Save Product", command=save_product, bootstyle=SUCCESS).grid(row=5, column=1, pady=10)
