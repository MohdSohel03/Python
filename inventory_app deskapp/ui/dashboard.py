import tkinter as tk
from ttkbootstrap import Toplevel, Label, Frame, Style
from ttkbootstrap.constants import *
from database import get_connection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def open_dashboard_window(root):
    win = Toplevel(root)
    win.title("Inventory Dashboard")
    win.geometry("800x600")
    win.resizable(False, False)

    style = Style("superhero")  # I can try 'darkly', 'cyborg', etc.

    container = Frame(win, padding=20)
    container.pack(fill="both", expand=True)

    # Cards frame
    stats_frame = Frame(container)
    stats_frame.pack(pady=10)

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch data
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(quantity) FROM products")
    total_qty = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(total) FROM transactions WHERE type = 'purchase'")
    total_purchase = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(total) FROM transactions WHERE type = 'sale'")
    total_sales = cursor.fetchone()[0] or 0

    conn.close()

    # Cards
    def create_card(parent, label, value, color):
        card = Frame(parent, padding=15, bootstyle=color)
        Label(card, text=label, font=("Segoe UI", 10), bootstyle="inverse-"+color).pack()
        Label(card, text=value, font=("Segoe UI", 16, "bold"), bootstyle="inverse-"+color).pack()
        return card

    create_card(stats_frame, "Total Products", total_products, "primary").grid(row=0, column=0, padx=10, pady=10)
    create_card(stats_frame, "Total Quantity", total_qty, "info").grid(row=0, column=1, padx=10, pady=10)
    create_card(stats_frame, "Purchase ₹", f"{total_purchase:.2f}", "success").grid(row=0, column=2, padx=10, pady=10)
    create_card(stats_frame, "Sales ₹", f"{total_sales:.2f}", "warning").grid(row=0, column=3, padx=10, pady=10)

    # Chart Section
    chart_frame = Frame(container)
    chart_frame.pack(pady=20)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    labels = ['Purchases', 'Sales']
    values = [total_purchase, total_sales]
    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=["#0d6efd", "#ffc107"])
    ax.set_title("Sales vs Purchases", fontsize=14)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Footer
    Label(container, text="Inventory Management Dashboard", font=("Segoe UI", 9), bootstyle="secondary").pack(side="bottom", pady=10)
