import tkinter as tk
from ttkbootstrap import Toplevel, Label, Button, Frame, Entry
from ttkbootstrap.constants import *
from tkinter import ttk
import csv
from datetime import datetime
from database import get_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def open_reports_window(root):
    win = Toplevel(root)
    win.title("Transaction Reports")
    win.geometry("800x700")
    win.resizable(True, True)

    # Frame setup
    frame = Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    # Heading
    Label(frame, text="Transaction Reports", font=("Segoe UI", 16, "bold")).pack(pady=10)

    # Filter Section
    filter_frame = Frame(frame)
    filter_frame.pack(pady=10)

    Label(filter_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
    start_date = Entry(filter_frame, bootstyle=PRIMARY)
    start_date.grid(row=0, column=1, padx=5)

    Label(filter_frame, text="End Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5)
    end_date = Entry(filter_frame, bootstyle=PRIMARY)
    end_date.grid(row=0, column=3, padx=5)

    def fetch_and_display_data():
        start = start_date.get()
        end = end_date.get()

        # Validate date format
        try:
            start_dt = datetime.strptime(start, '%Y-%m-%d') if start else None
            end_dt = datetime.strptime(end, '%Y-%m-%d') if end else None
        except ValueError:
            Label(frame, text="Invalid date format! Use YYYY-MM-DD.", bootstyle="danger").pack(pady=5)
            return

        # Clear previous results
        for item in treeview.get_children():
            treeview.delete(item)

        # Fetch data with date filter
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM transactions"
        params = []

        if start_dt and end_dt:
            query += " WHERE date BETWEEN ? AND ? ORDER BY date DESC"
            params = [start_dt, end_dt]
        elif start_dt:
            query += " WHERE date >= ? ORDER BY date DESC"
            params = [start_dt]
        elif end_dt:
            query += " WHERE date <= ? ORDER BY date DESC"
            params = [end_dt]

        cursor.execute(query, params)
        transactions = cursor.fetchall()

        for transaction in transactions:
            treeview.insert("", "end", values=transaction)

        conn.close()

        # Display Chart for Purchases and Sales
        if transactions:
            total_purchase = sum([t[5] for t in transactions if t[3] == "purchase"])
            total_sales = sum([t[5] for t in transactions if t[3] == "sale"])

            fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
            ax.bar(['Purchases', 'Sales'], [total_purchase, total_sales], color=["#0d6efd", "#ffc107"])
            ax.set_title("Total Purchases vs Sales", fontsize=14)
            ax.set_ylabel("Amount (₹)")
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

    # Button to fetch and filter transactions
    filter_button = Button(frame, text="Filter", command=fetch_and_display_data, bootstyle=INFO)
    filter_button.pack(pady=10)

    # Table for displaying transactions
    columns = ("Transaction ID", "Product ID", "Product Name", "Type", "Quantity", "Total", "Date")
    treeview = ttk.Treeview(frame, columns=columns, show="headings")
    treeview.pack(fill="both", expand=True)

    # Column definitions
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=150, anchor=CENTER)

    # Export to CSV
    def export_to_csv():
        with open('transactions_report.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)  # Write header
            for transaction in treeview.get_children():
                writer.writerow(treeview.item(transaction)["values"])

        Label(frame, text="Report Exported Successfully!", bootstyle="success").pack(pady=5)

    # Button to export to CSV
    export_button = Button(frame, text="Export to CSV", command=export_to_csv, bootstyle=SUCCESS)
    export_button.pack(pady=10)
