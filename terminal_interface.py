import datetime
import sys
from decimal import Decimal
from database import create_table, add_transaction as db_add_transaction, view_transactions as db_view_transactions, export_data as db_export_data
from currency_converter import convert_currency
from gui_interface import FinanceTrackerApp
import tkinter as tk

# Ensure table exists
create_table()

def main():
    print("Choose an interface:")
    print("1. Terminal")
    print("2. GUI")
    
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        run_terminal_interface()
    elif choice == "2":
        run_gui_interface()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

def add_transaction(amount, category, description, date, currency):
    """Add a transaction to the database."""
    return db_add_transaction(amount, category, description, date, currency)

def view_transactions(filter_by='', filter_value=''):
    """Retrieve and format transactions from the database."""
    transactions = db_view_transactions(filter_by, filter_value)
    result = []
    for row in transactions:
        try:
            transaction_id, date, description, amount, currency, category = row
            # Handle the date formatting
            formatted_date = date.strftime('%Y-%m-%d') if isinstance(date, datetime.date) else str(date)
            # Handle the Decimal amount and ensure it is rounded correctly
            if isinstance(amount, Decimal):
                formatted_amount = round(float(amount), 2)
            else:
                formatted_amount = round(float(amount), 2)  # Ensure amount is a float
            result.append(f"ID: {transaction_id}, Date: {formatted_date}, Description: {description}, Amount: {formatted_amount:.2f}, Currency: {currency}, Category: {category}")
        except Exception as e:
            result.append(f"Error processing row: {row}. Error: {e}")
    return result

def export_data(format):
    """Export transactions to CSV or JSON."""
    return db_export_data(format)

def run_terminal_interface():
    """Run the terminal interface for finance tracker."""
    while True:
        print("\nFinance Tracker")
        print("1. Add Transaction")
        print("2. Convert Currency")
        print("3. View Transactions")
        print("4. Export Data")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == '1':
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                description = input("Enter description: ")
                date = input("Enter date (YYYY-MM-DD): ")
                currency = input("Enter currency: ")
                result = add_transaction(amount, category, description, date, currency)
                print(result)
            except ValueError:
                print("Invalid amount.")

        elif choice == '2':
            try:
                amount = float(input("Enter amount: "))
                from_currency = input("Enter from currency: ")
                to_currency = input("Enter to currency: ")
                result = convert_currency(amount, from_currency, to_currency)
                if isinstance(result, str) and result.startswith("Error:"):
                    print(result)
                else:
                    print(f"{amount} {from_currency} = {result:.2f} {to_currency}")  # Format to 2 decimal places
            except ValueError:
                print("Invalid amount.")

        elif choice == '3':
            #filter_by = input("Filter by (date/category/amount) or leave empty: ").strip().lower()
            #filter_value = input("Enter filter value or leave empty: ").strip()
            transactions = view_transactions()
            for transaction in transactions:
                print(transaction)

        elif choice == '4':
            format = input("Enter format (csv/json): ").strip().lower()
            result = export_data(format)
            print(result)

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

def run_gui_interface():
    """Run the GUI interface for finance tracker."""
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
