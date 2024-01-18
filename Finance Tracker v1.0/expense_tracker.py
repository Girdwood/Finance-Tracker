from expense import Expense
import calendar
import datetime
import pickle


# In-memory budget dictionary
budget_data = {'budget': 2000}


def load_budget():
    try:
        with open("budget.pkl", "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return {'budget': 2000}


def save_budget(new_budget):
    with open("budget.pkl", "wb") as file:
        pickle.dump(new_budget, file)


def update_budget():
    global budget_data
    try:
        new_budget = float(input("Enter the new budget: "))
        budget_data['budget'] = new_budget
        save_budget(budget_data)
        print(f"Budget updated to: ${new_budget:.2f}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def main():
    global budget_data
    loaded_budget = load_budget()
    budget_data.update(loaded_budget)

    update_input = input("Do you want to update your budget? ").lower()

    if update_input == 'yes':
        update_budget()

    else:
        print(f"\n🎯 Running Expense Tracker!\n")

    # Get user input for expense.
    expense = get_user_expense()

    # Define expense_file_path here or pass it as a parameter to save_expense_to_file
    expense_file_path = "expenses.csv"

    # Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget_data)

    while True:
        continue_input = input(
            "Do you want to enter another expense? (yes/no): ").lower()

        if continue_input != 'yes':
            print("Goodbye")
            break

        if __name__ == "__main__":
            get_user_expense()


def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(
            input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding='utf-8', newline='') as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget_data):
    print(f"🎯 Summarizing User Expense")
    expenses = []
    with open(expense_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: £{amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: £{total_spent:.2f}")

    remaining_budget = budget_data['budget'] - total_spent
    print(f"✅ Budget Remaining: £{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: £{daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
