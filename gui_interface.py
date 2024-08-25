import tkinter as tk
from tkinter import ttk, messagebox
from database import add_transaction as db_add_transaction, view_transactions as db_view_transactions, export_data as db_export_data
from currency_converter import convert_currency
import datetime

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI widgets."""
        self.tab_control = ttk.Notebook(self.root)

        # Add Transaction Tab
        self.add_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.add_tab, text="Add Transaction")
        self.create_add_transaction_widgets()

        # View Transactions Tab
        self.view_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.view_tab, text="View Transactions")
        self.create_view_transaction_widgets()

        # Export Data Tab
        self.export_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.export_tab, text="Export Data")
        self.create_export_data_widgets()

        # Currency Converter Tab
        self.convert_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.convert_tab, text="Currency Converter")
        self.create_currency_converter_widgets()

        self.tab_control.pack(expand=1, fill="both")

    def create_add_transaction_widgets(self):
        """Create widgets for adding a transaction."""
        ttk.Label(self.add_tab, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
        self.amount_entry = ttk.Entry(self.add_tab)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.add_tab, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        self.category_entry = ttk.Entry(self.add_tab)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.add_tab, text="Description:").grid(row=2, column=0, padx=10, pady=5)
        self.description_entry = ttk.Entry(self.add_tab)
        self.description_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.add_tab, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.date_entry = ttk.Entry(self.add_tab)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.add_tab, text="Currency:").grid(row=4, column=0, padx=10, pady=5)
        self.currency_entry = ttk.Entry(self.add_tab)
        self.currency_entry.grid(row=4, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(self.add_tab, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def create_view_transaction_widgets(self):
        """Create widgets for viewing transactions."""
        self.view_tree = ttk.Treeview(self.view_tab, columns=("id", "amount", "category", "description", "date", "currency"), show="headings")
        self.view_tree.heading("id", text="ID")
        self.view_tree.heading("amount", text="Amount")
        self.view_tree.heading("category", text="Category")
        self.view_tree.heading("description", text="Description")
        self.view_tree.heading("date", text="Date")
        self.view_tree.heading("currency", text="Currency")
        self.view_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.filter_entry = ttk.Entry(self.view_tab)
        self.filter_entry.pack(side=tk.LEFT, padx=10, pady=10)

        self.filter_button = ttk.Button(self.view_tab, text="View", command=self.filter_transactions)
        self.filter_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.refresh_button = ttk.Button(self.view_tab, text="Refresh", command=self.load_transactions)
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_export_data_widgets(self):
        """Create widgets for exporting data."""
        self.export_format = tk.StringVar()
        self.export_format.set("csv")

        ttk.Label(self.export_tab, text="Format (csv/json):").grid(row=0, column=0, padx=10, pady=5)
        self.format_entry = ttk.Entry(self.export_tab, textvariable=self.export_format)
        self.format_entry.grid(row=0, column=1, padx=10, pady=5)

        self.export_button = ttk.Button(self.export_tab, text="Export Data", command=self.export_data)
        self.export_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def create_currency_converter_widgets(self):
        """Create widgets for currency conversion."""
        ttk.Label(self.convert_tab, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
        self.convert_amount_entry = ttk.Entry(self.convert_tab)
        self.convert_amount_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.convert_tab, text="From Currency:").grid(row=1, column=0, padx=10, pady=5)
        self.from_currency_entry = ttk.Entry(self.convert_tab)
        self.from_currency_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.convert_tab, text="To Currency:").grid(row=2, column=0, padx=10, pady=5)
        self.to_currency_entry = ttk.Entry(self.convert_tab)
        self.to_currency_entry.grid(row=2, column=1, padx=10, pady=5)

        self.convert_button = ttk.Button(self.convert_tab, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = ttk.Label(self.convert_tab, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_transaction(self):
        """Add a transaction to the database."""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            date = datetime.datetime.strptime(self.date_entry.get(), '%Y-%m-%d').date()
            currency = self.currency_entry.get()
            result = db_add_transaction(amount, category, description, date, currency)
            messagebox.showinfo("Success", result)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def filter_transactions(self):
        """Filter transactions based on input."""
        filter_by = self.filter_entry.get()
        transactions = db_view_transactions(filter_by)
        for row in self.view_tree.get_children():
            self.view_tree.delete(row)
        for transaction in transactions:
            self.view_tree.insert("", tk.END, values=transaction)

    def load_transactions(self):
        """Load all transactions into the tree view."""
        transactions = db_view_transactions()
        for row in self.view_tree.get_children():
            self.view_tree.delete(row)
        for transaction in transactions:
            self.view_tree.insert("", tk.END, values=transaction)

    def export_data(self):
        """Export data to CSV or JSON format."""
        format_type = self.export_format.get().strip().lower()
        result = db_export_data(format_type)
        messagebox.showinfo("Export Result", result)

    def convert_currency(self):
        """Convert currency based on input."""
        try:
            amount = float(self.convert_amount_entry.get())
            from_currency = self.from_currency_entry.get()
            to_currency = self.to_currency_entry.get()
            converted_amount = convert_currency(amount, from_currency, to_currency)
            self.result_label.config(text=f"{amount} {from_currency} = {converted_amount} {to_currency}")
        except ValueError as e:
            self.result_label.config(text=f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
