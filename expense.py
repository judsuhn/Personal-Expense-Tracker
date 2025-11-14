from datetime import date
from datetime import datetime
import json

menu = ("""
=== Expense Tracker ===
1. Add New Expense
2. View All Expenses
3. Remove Expense from List
4. View Expenses by Category
5. View Monthly Summary
6. Exit
""")

expenses_type = ["food", "gas", "groceries", "travel", 'other']


def save_expense():
    try:
        with open('expenses.json', 'w') as file:
            json.dump(expenses, file, indent=2)
    except IOError as e:
        print(f"Error saving expenses: {e}")
    except Exception as e:
        print(f"Unexpected error while saving: {e}")


def load_expense():
    try:
        with open('expenses.json', "r") as file:
            content = file.read().strip()

            if not content:
                print("Expense file is empty, starting fresh.")
                return []

            try:
                data = json.loads(content)

                if not isinstance(data, list):
                    print(
                        "Warning: Invalid data format in expenses.json. Starting fresh.")
                    return []

                valid_expenses = []
                for exp in data:
                    if isinstance(exp, dict) and all(key in exp for key in ['amount', 'category', 'date', 'description']):
                        valid_expenses.append(exp)
                    else:
                        print(
                            f"Warning: Skipping invalid expense entry: {exp}")

                return valid_expenses

            except json.JSONDecodeError as e:
                print(
                    f"Error: expenses.json contains invalid JSON format: {e}")
                print("Creating backup and starting fresh.")

                try:
                    with open("expenses_backup.json", "w") as backup:
                        backup.write(content)
                    print("Corrupted file backed up as expenses_backup.json")
                except:
                    pass

                return []

    except FileNotFoundError:
        print("File does not exist, please add an expense if this is your first time running the program.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


expenses = load_expense()


def add_expense():
    while True:
        try:
            amount_input = float(input('How Much was this expense? '))
            break
        except ValueError:
            print('Try again')

    category_input = input('''What was the category of this expense?
                                 Food
                                 Gas
                                 Groceries
                                 Travel
                                 Other
                                 ''').lower()
    while True:
        if category_input not in expenses_type:
            print('Please input a valid category.')
            category_input = input('Try again: ').lower()
        else:
            break

    expense_date = input(
        'Input today\'s date format YYYY-MM-DD or Press Enter for today\'s date ')
    while True:
        try:
            if expense_date == "":
                expense_date = str(date.today())
            else:
                datetime.strptime(expense_date, "%Y-%m-%d")
            break
        except ValueError:
            print('Enter the date in the proper format.')
            expense_date = input(
                "Please try again with the format YYYY-MM-DD: ")

    description = input('What was the description of this expense? ').lower()
    new_expense = {
        "amount": amount_input,
        "category": category_input,
        "date": expense_date,
        "description": description
    }
    expenses.append(new_expense)
    save_expense()
    print("Here is your added expense: ")
    print(
        f"${new_expense['amount']} | {new_expense['category'].capitalize()} | {new_expense['date']} | {new_expense['description'].capitalize()}")


def view_expense():
    if not expenses:
        print('There are no expenses recorded.')
        return

    print('=== All Expenses ===')
    for i, exp in enumerate(expenses, start=1):
        print(
            f"{i}. ${exp['amount']} | {exp['category'].capitalize()} | {exp['date']} | {exp['description'].capitalize()}")


def remove_expense():
    if not expenses:
        print('No Expenses to Remove')
        return

    print("Which expense would you like to remove?")
    for i, exp in enumerate(expenses, start=1):
        print(
            f'{i}. ${exp['amount']} | {exp['category']} | {exp['date']} | {exp['description'].capitalize()}')
    try:
        remove_option = int(input('> '))
        if 1 <= remove_option <= len(expenses):
            removed = expenses.pop(remove_option - 1)
            save_expense()
            print('Expense Successfully Deleted!')
    except ValueError:
        print('Invalid Option, Please Try again.')


def view_category():
    if not expenses:
        print('There are no expenses recorded.')
        return

    category = input('Select which category you want to sort by: ').lower()

    print(f'=== Expenses by Category: {category}')
    found_any = False

    for exp in expenses:
        if exp["category"] == category:
            found_any = True
            print(
                f'${exp['amount']} | {exp['date']} | {exp['description'].capitalize()}')

    if not found_any:
        print('No expenses found in this category')


def view_monthly():
    if not expenses:
        print('No expenses recorded.')
        return

    today = date.today()
    current_month = today.month
    current_year = today.year

    total_this_month = 0
    category_totals = {}

    for exp in expenses:
        exp_date = datetime.strptime(exp['date'], "%Y-%m-%d").date()
        if exp_date.month == current_month and exp_date.year == current_year:
            total_this_month += exp['amount']
            category_totals[exp['category']] = category_totals.get(
                exp['category'], 0) + exp['amount']

    print(
        f'=== Monthly Category Summary For: {today.strftime('%B %Y')} ===')
    print(f"This Month's Total is ${total_this_month:.2f}")
    print(f"Breakdown by category:")
    if category_totals:
        for category, total in category_totals.items():
            print(f" {category.capitalize()}: {total:.2f}")
    else:
        print("No expenses found in this category.")


def display_menu():
    while True:
        print(menu)
        try:
            choice = int(input("What would you like to choose? "))
        except ValueError:
            print('Please choose a valid response')
            continue

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expense()
        elif choice == 3:
            remove_expense()
        elif choice == 4:
            view_category()
        elif choice == 5:
            view_monthly()
        elif choice == 6:
            print('Thank you for using our program.')
            break
        else:
            print('Invalid selection, please try again.')


display_menu()
