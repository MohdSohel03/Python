# 📦 Inventory Management System (Python + ttkbootstrap)

A modern desktop-based **Inventory Management System** built with Python using `ttkbootstrap` for a professional UI. This application helps businesses manage products, record transactions, generate reports, and monitor inventory data via a sleek dashboard.

---

## 🧩 Features

- 🛒 **Manage Products**: Add, update, or delete product entries.
- 💰 **Record Transactions**: Log sales or purchases with real-time updates.
- 📊 **Dashboard**: Visualize inventory data (stock levels, top-selling items, etc.).
- 🧾 **Reports**: Generate and view detailed inventory and transaction reports.
- 🌙 **Modern UI**: Built with `ttkbootstrap` using the **Darkly** theme for a clean, dark interface.
- 🗃️ **Database Integration**: Automatically sets up and connects to a local SQLite database.

---

## 🛠️ Technologies Used

- Python 3
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) – Stylish themed widgets based on Tkinter
- Tkinter – Core GUI framework
- SQLite – Local database for storing inventory and transactions
- Modular File Structure – Separate UI modules for better code organization

---

## 📂 Project Structure

inventory_management/
├── main.py # Main application launcher
├── database.py # Database setup and connection
├── ui/
│ ├── products.py # Product management window
│ ├── transactions.py # Transaction window
│ ├── dashboard.py # Dashboard window
│ └── reports.py # Reports window
└── README.md # Project documentation
---

## 🚀 Getting Started

### 1. Clone the repository
git clone https://github.com/MohdSohel03/Python/tree/54db63e9eedf887cd36174442fef668d93bf10ce/inventory_app%20deskapp

cd inventory-management-system

### 2. Install dependencies
Install `ttkbootstrap` (and any other required packages):
pip install ttkbootstrap

### 3. Run the application
python main.py

---

## ✅ How It Works

- On launch, the system initializes the local database (`setup_database()`).
- The main window offers buttons to navigate to each module:
  - **Manage Products**
  - **Record Transaction**
  - **View Dashboard**
  - **View Reports**
- Each feature is handled by a separate file in the `ui/` folder for clarity and scalability.

---

## 🔧 Future Enhancements

- PDF/Excel export for reports
- Search/filter functionality
- User authentication
- Inventory alerts for low stock
- Multi-user access or web integration (Flask or Django)

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙋‍♂️ Contact

**Developer**: Mohd Sohel Ansari  
**Email**: Uplaoding Soon 
**GitHub**: https://github.com/MohdSohel03

