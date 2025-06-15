import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.products import open_product_window
from ui.transactions import open_transaction_window
from database import setup_database
from ui.dashboard import open_dashboard_window
from ui.reports import open_reports_window


def launch_app():
    setup_database()
    app = ttk.Window(themename="darkly")
    app.title("Inventory Management System")
    app.geometry("800x500")

    ttk.Label(app, text="Inventory Management System", font=("Segoe UI", 22)).pack(pady=20)

    ttk.Button(app, text="View Reports", command=lambda: open_reports_window(app), bootstyle=INFO).pack(pady=10)
    ttk.Button(app, text="Manage Products", command=lambda: open_product_window(app), bootstyle=PRIMARY).pack(pady=10)
    ttk.Button(app, text="Record Transaction", command=lambda: open_transaction_window(app), bootstyle=SUCCESS).pack(pady=10)
    ttk.Button(app, text="View Dashboard", command=lambda: open_dashboard_window(app), bootstyle=INFO).pack(pady=10)
    app.mainloop()

if __name__ == "__main__":
    launch_app()
