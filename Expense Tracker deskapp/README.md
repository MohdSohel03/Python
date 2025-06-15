# 💸 Expense Tracker - Dark Mode (Tkinter + Matplotlib)

A sleek, dark-themed desktop Expense Tracker built using **Python**, **Tkinter**, and **Matplotlib**. Easily add, edit, delete, filter, and visualize your daily expenses by category. Designed with usability in mind — smooth fade-in effect, category filtering, and persistent data storage.

## 📌 Features

- 📝 Add & Edit Expenses: Track your spending with fields like date, time, category, amount, and notes.
- ❌ Delete Entries: Easily delete any selected expense from the list.
- 📅 Filter Expenses: Filter by category or date to quickly find specific entries.
- 📊 Visual Charts: View a bar chart of total spending per category.
- 💾 Data Persistence: Expenses are saved locally using the pickle module.
- 🌙 Dark Mode UI: Clean and modern interface styled for night-time use.
- ✨ Fade-In Animation: Smooth transition effect when the app loads.

## 🛠️ Technologies Used

- Python 3
- Tkinter (GUI)
- ttk & ttk.Style
- matplotlib
- pickle (for file storage)
- tkcalendar (Date picker)

## 📦 Installation

1. Clone the repository:
git clone https://github.com/MohdSohel03/Python/tree/cebd047a2964bb814bc271f1609f399daa92f4be/Expense%20Tracker%20deskapp
2. Install required dependencies:
pip install tkcalendar matplotlib
3. Run the app:
python main.py

## 🧠 How It Works

- Data is stored in a file named `expenses.pkl` using Python’s `pickle` module.
- You can add, edit, or delete entries via the form.
- The list auto-refreshes and calculates total expenses.
- Charts are generated using matplotlib.
- GUI is built with Tkinter and styled with a custom dark theme.

## 📂 File Structure

expense_tracker_dark/
├── expense_tracker.py # Main script
├── expenses.pkl # Auto-created to store your data
└── README.md # Project info

markdown
Copy
Edit

## 🚀 Future Improvements

- Export to CSV/Excel
- Monthly summaries or graphs
- Light/dark mode toggle
- Authentication and user profiles
- Mobile version using Kivy or Flutter

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements or new features.

## 📄 License

This project is licensed under the MIT License.

## 📧 Contact

**Developer**: Mohd Sohel Ansari  
**Email**: Getting soon 
**GitHub**: https://github.com/MohdSohel03
