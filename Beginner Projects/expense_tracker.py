import datetime

expenses = []

def show_menu():
    print("\n💸 Personal Expense Tracker")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Total Spent")
    print("4. Exit")

def add_expense():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.date.today().isoformat()

    time = input("Enter time (HH:MM) or press Enter for current time: ")
    if not time:
        time = datetime.datetime.now().strftime("%H:%M")

    category = input("Enter category (e.g., Food, Travel, Bills): ")
    amount = float(input("Enter amount spent: ₹"))
    note = input("Add a note (optional): ")

    expense = {
        "date": date,
        "time": time,
        "category": category,
        "amount": amount,
        "note": note
    }

    expenses.append(expense)
    print("✅ Expense added!")

def view_expenses():
    if not expenses:
        print("No expenses recorded.")
    else:
        print("\n📃 Expense History:")
        for i, exp in enumerate(expenses, 1):
            print(f"{i}. [{exp['date']} {exp['time']}] ₹{exp['amount']} - {exp['category']} ({exp['note']})")

def total_spent():
    total = sum(exp["amount"] for exp in expenses)
    print(f"💰 Total Spent: ₹{total}")

# Main Loop
while True:
    show_menu()
    choice = input("Choose an option (1-4): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        total_spent()
    elif choice == "4":
        print("👋 Exiting... Stay financially smart!")
        break
    else:
        print("⚠️ Invalid choice. Try again.")
