import requests
import os
import datetime
import pickle
import csv
from prettytable import PrettyTable



class MonzoFinanceTracker:
    def __init__(self):
        self.budget_data = {'budget': 2000}
        self.account_id = None
        self.account_token = None
        self.API_URL = 'https://api.monzo.com/'

    def fetch_user_credentials(self):
        print("Welcome to the Monzo API Finance Tracker\n")

        self.account_id = input("Please enter your Monzo API Playground ID: ")
        self.account_token = input("Please enter your Monzo API Playground Token: ")
        print('\n')

    def main_menu(self):
        while True:
            print("1. Update your Budget")
            print("2. Retrieve and update finance data from Monzo")
            print("3. Display current expenses from Monzo")
            print("4. Delete all retrieved financial data from the program")
            print("5. Exit")

            menu_choice = input("Please Enter One of the Following: ")

            if menu_choice == '1':
                self.budget()
            elif menu_choice == '2':
                user_transactions = self.get_transactions()
                if user_transactions:
                    self.save_to_csv(user_transactions)
                else:
                    print("Failed to retrieve transactions.")
            elif menu_choice == '3':
                self.display_expenses('monzo_transactions.csv')
            elif menu_choice == '4':
                self.delete_expenses('monzo_transactions.csv')
            elif menu_choice == '5':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def budget(self):
        try:
            new_budget = float(input("Enter the new budget: "))
            self.budget_data['budget'] = new_budget
            self.save_budget(self.budget_data)
            print(f"\nBudget updated to: ${new_budget:.2f}\n")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")

    def load_budget(self):
        try:
            with open("MonzoBudget.pkl", "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return {'budget': 2000}

    def save_budget(self, new_budget):
        with open("MonzoBudget.pkl", "wb") as file:
            pickle.dump(new_budget, file)

    def get_transactions(self):
        headers = {'Authorization': f'Bearer {self.account_token}'}
        transactions_response = requests.get(
            f'{self.API_URL}transactions?account_id={self.account_id}',
            headers=headers
        )

        if transactions_response.status_code == 200:
            return transactions_response.json()['transactions']
        else:
            print(f"\nError: {transactions_response.status_code}\n")
            print("Please make sure your user id and token are correct\n")
            return None

    def format_currency(self, amount):
        return round(amount / 100, 2)

    def save_to_csv(self, transactions, filename='monzo_transactions.csv'):
        if not transactions:
            print("No transactions to save.")
            return

        desired_fields = ['created', 'amount', 'description', 'category']

        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=desired_fields)
            writer.writeheader()

            for transaction in transactions:
                transaction['amount'] = self.format_currency(transaction['amount'])
                selected_data = {field: transaction[field] for field in desired_fields}
                writer.writerow(selected_data)

        print(f"\nSelected information saved to {filename}.\n")

    def display_expenses(self, filename='monzo_transactions.csv'):
        try:
            with open(filename, mode='r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                table = PrettyTable(header)
                table.align = 'l'

                total_spent = 0

                for row in reader:
                    row[0] = row[0].split('T')[0]
                    row[1] = f'£{row[1]}'
                    total_spent += float(row[1].replace('£', ''))
                    table.add_row(row)

                print(table)
                print('\n')

                remaining_budget = self.budget_data['budget'] - total_spent

                now = datetime.datetime.now()
                remaining_budget_month = remaining_budget / now.day * 30
                print(f"Your Budget was set at £{self.budget_data['budget']:.2f}")
                print(self.green(f"\nRemaining Budget for the Month: £{remaining_budget_month:.2f}\n"))

        except FileNotFoundError:
            print(f"\nFile '{filename}' not found. Please save transactions first.\n")

    def delete_expenses(self, filename='monzo_transactions.csv'):
        try:
            os.remove(filename)
            print(f"\nExpenses deleted successfully.\n")
        except FileNotFoundError:
            print(f"\nFile '{filename}' not found. No expenses to delete.\n")
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

   
    @staticmethod
    def green(text):
        return f"\033[92m{text}\033[0m"


if __name__ == '__main__':
    finance_tracker = MonzoFinanceTracker()
    finance_tracker.fetch_user_credentials()
    finance_tracker.main_menu()