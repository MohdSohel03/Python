# todo_app.py

tasks = []

import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def show_menu():
    print("\nTo-Do List App")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Exit")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def add_task():
    task = input("Enter the task: ")
    tasks.append(task)
    print(f"Task added: {task}")

def remove_task():
    view_tasks()
    try:
        index = int(input("Enter the task number to remove: "))
        removed = tasks.pop(index - 1)
        print(f"Removed: {removed}")
    except (IndexError, ValueError):
        print("Invalid input!")

while True:
    show_menu()
    choice = input("Choose an option (1-4): ")
    if choice == "1":
        view_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        remove_task()
    elif choice == "4":
        print("👋 Exiting... Bye!")
        break
    else:
        print("Invalid choice. Please select from 1 to 4.")
