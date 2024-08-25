import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')

def get_connection():
    """
    Establish a connection to the PostgreSQL database.
    """
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

def create_table():
    """Create the transactions table if it does not exist."""
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

def add_transaction(amount, category, description, date, currency):
    """Add a new transaction to the database."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transactions (amount, category, description, date, currency)
                VALUES (%s, %s, %s, %s, %s)
            """, (amount, category, description, date, currency))
            conn.commit()
    return "Transaction added successfully."

def view_transactions(filter_by=None, filter_value=None):
    """Retrieve transactions based on filter criteria."""
    query = "SELECT * FROM transactions"
    params = []
    if filter_by and filter_value:
        query += f" WHERE {filter_by} = %s"
        params.append(filter_value)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

def export_data(format_type):
    """Export data in the specified format (e.g., CSV, JSON)."""
    # Implementation of data export functionality can be added based on format_type
    return "Data exported successfully."