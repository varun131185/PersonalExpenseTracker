import csv
import os
from datetime import datetime

# Global list to store expenses
monthly_expenses = []
monthly_budget = 0.0


# ------------------ Add an expense ------------------ #
def add_expense():
    # taking user input for date with format validation
    while True:
        try:
            date = input("Enter the date (YYYY-MM-DD): ").strip()
            datetime.strptime(date, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date! Please enter a date in correct format.")

    # taking user input for expense category without any validation
    category = input("Enter the category (e.g., Food, Travel): ").strip()

    # taking user input for amount as valid integer or float value
    while True:
        try:
            amount = float(input("Enter the amount spent: ").strip())
            break
        except ValueError:
            print("Invalid amount! Please enter a number.")

    # taking user input for brief description without any validation
    description = input("Enter a brief description: ").strip()

    # creating expense as dictionary
    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }

    # adding expense as dictionary in monthly expense list
    monthly_expenses.append(expense)

    print("Expense added successfully!")


# ------------------ View expenses ------------------ #
def view_expenses():
    if not monthly_expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- Expenses ---")
    required_keys = ['date', 'category', 'amount', 'description']
    start = 1
    for expense in monthly_expenses:
        # Check if all required keys are present in the current dictionary
        if all(key in expense for key in required_keys):
            # Identify incomplete entry
            valueFlag = False
            for value in expense.values():
                if value is None or value == 'None' or str(value) == '':
                    valueFlag = True
            if valueFlag:
                print(f"{start}. Incomplete expense data, Skipping incomplete entry: {expense}")
            else:
                # Perform operations with the dictionary, knowing all keys exist
                print(f"{start}. Date: {expense['date']} | Category: {expense['category']} | "
                  f"Amount: {expense['amount']} | Description: {expense['description']}")
        else:
            # Identify incomplete entry
            print(f"{start}. Incomplete expense data, Skipping incomplete entry: {expense}")
        start = start + 1
    print("----------------\n")


# ------------------ Set and track budget ------------------ #
def set_budget():
    global monthly_budget
    try:
        monthly_budget = float(input("Enter your monthly budget: ").strip())
        print(f"Monthly budget set to {monthly_budget}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def track_budget():
    if monthly_budget == 0:
        print("Budget not set yet. Please set a budget first.")
        return

    total_expenses = 0.0
    # sum(exp['amount'] for exp in monthly_expenses)
    for exp in monthly_expenses:
        try:
            total_expenses += float(exp['amount'])
        except TypeError:
            print("Incorrect amount value in Expenses, so skipping the entry.")
        except ValueError:
            print("Incorrect amount value in Expenses, so skipping the entry.")


    print(f"Total expenses so far: {total_expenses}")

    if total_expenses > monthly_budget:
        print("⚠️ Warning: You have exceeded your budget!")
    else:
        remaining = monthly_budget - total_expenses
        print(f"✅ You have {remaining} left for the month.")


# ------------------ Save & Load expenses ------------------ #
def save_expenses(filename="expenses.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
        writer.writeheader()
        writer.writerows(monthly_expenses)
    print("Expenses saved successfully.")


def load_expenses(filename="expenses.csv"):
    global monthly_expenses
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            monthly_expenses = [row for row in reader]
            # Convert amount to float
            for exp in monthly_expenses:
                try:
                    exp['amount'] = float(exp['amount'])
                    exp['date'] = str(exp['date'])
                    exp['category'] = str(exp['category'])
                    exp['description'] = str(exp['description'])
                except TypeError:
                    print("Incorrect entries in Expenses csv file.")
                except ValueError:
                    print("Incorrect entries in Expenses csv file.")
        print("Expenses loaded successfully.")
    else:
        monthly_expenses = []


# ------------------ Interactive menu ------------------ #
def interactive_Menu():
    load_expenses()  # Load previous expenses on start
    while True:
        print("\n==== Personal Expense Tracker ====")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Set/Track budget")
        print("4. Save expenses")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            if monthly_budget == 0:
                set_budget()
            track_budget()
        elif choice == '4':
            save_expenses()
        elif choice == '5':
            save_expenses()
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option! Please choose between 1 and 5.")


# ------------------ Run the program ------------------ #
if __name__ == "__main__":
    interactive_Menu()
