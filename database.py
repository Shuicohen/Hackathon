import psycopg2
from dotenv import load_dotenv
import os
import json
import csv
from decimal import Decimal
from datetime import date, datetime

# Load environment variables
load_dotenv()

# Database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

# Establish a connection to the PostgreSQL database.
def get_connection():
    try:
        connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

# Create the transactions table if it does not exist. 
def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    amount DECIMAL NOT NULL,
                    category VARCHAR(50),
                    description TEXT,
                    date DATE,
                    currency VARCHAR(10)
                )
            """)
            conn.commit()

# Add a new transaction to the database.
def add_transaction(amount, category, description, date, currency):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transactions (amount, category, description, date, currency)
                VALUES (%s, %s, %s, %s, %s)
            """, (amount, category, description, date, currency))
            conn.commit()
    return "Transaction added successfully."

# Retrieve transactions based on filter criteria.
def view_transactions(filter_by=None, filter_value=None):
    query = "SELECT * FROM transactions"
    params = []
    if filter_by and filter_value:
        query += f" WHERE {filter_by} = %s"
        params.append(filter_value)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

# Serialize a transaction for JSON export.
def serialize_transaction(transaction):
    transaction_id, transaction_date, description, amount, currency, category = transaction
    return {
        'id': transaction_id,
        'date': transaction_date.isoformat() if isinstance(transaction_date, date) else str(transaction_date),
        'description': description,
        'amount': float(amount) if isinstance(amount, Decimal) else amount,
        'currency': currency,
        'category': category
    }


# Export data in the specified format (e.g., CSV, JSON).
def export_data(format):
    connection = get_connection()  # Assuming you have a function to get a DB connection
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        
        if format == 'csv':
            with open('transactions.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Date', 'Description', 'Amount', 'Currency', 'Category'])
                for transaction in transactions:
                    writer.writerow(transaction)
            return "Data exported to transactions.csv"

        elif format == 'json':
            transactions_serializable = [serialize_transaction(t) for t in transactions]
            with open('transactions.json', 'w') as file:
                json.dump(transactions_serializable, file, indent=4)
            return "Data exported to transactions.json"
        
        else:
            return "Unsupported format. Please use 'csv' or 'json'."
    
    except Exception as e:
        return f"Error exporting data: {e}"
    
    finally:
        cursor.close()
        connection.close()
