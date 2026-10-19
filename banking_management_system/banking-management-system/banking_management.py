"""
Banking Management System — beginner Python + SQLite project.
This is a local educational demo only, not a real banking service.
"""
import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "banking.db"
STARTING_CUSTOMERS = [
    (1001, "Aarav Sharma", "aarav.sharma@example.com", "9000001001"),
    (1002, "Diya Patil", "diya.patil@example.com", "9000001002"),
    (1003, "Kabir Deshmukh", "kabir.deshmukh@example.com", "9000001003"),
    (1004, "Anaya Joshi", "anaya.joshi@example.com", "9000001004"),
    (1005, "Ishaan Kulkarni", "ishaan.kulkarni@example.com", "9000001005"),
]
STARTING_ACCOUNTS = [
    (2001, 1001, "Savings", 25000.00),
    (2002, 1002, "Current", 62000.00),
    (2003, 1003, "Savings", 14500.00),
    (2004, 1004, "Savings", 38000.00),
    (2005, 1005, "Current", 51000.00),
]

def connect():
    """Open a connection and enable foreign-key checks."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database():
    """Create tables and insert demo records only when tables are empty."""
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                account_type TEXT NOT NULL CHECK(account_type IN ('Savings', 'Current')),
                balance REAL NOT NULL CHECK(balance >= 0),
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Deposit', 'Withdrawal', 'Transfer In', 'Transfer Out')),
                amount REAL NOT NULL CHECK(amount > 0),
                description TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(account_id) REFERENCES accounts(account_id)
            )
        """)
        customer_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if customer_count == 0:
            conn.executemany(
                "INSERT INTO customers(customer_id, full_name, email, phone) VALUES (?, ?, ?, ?)",
                STARTING_CUSTOMERS
            )
            conn.executemany(
                "INSERT INTO accounts(account_id, customer_id, account_type, balance) VALUES (?, ?, ?, ?)",
                STARTING_ACCOUNTS
            )

def list_accounts():
    with connect() as conn:
        return conn.execute("""
            SELECT a.account_id, c.full_name, a.account_type, a.balance
            FROM accounts a JOIN customers c ON c.customer_id = a.customer_id
            ORDER BY a.account_id
        """).fetchall()

def list_transactions(account_id=None):
    query = """
        SELECT transaction_id, account_id, transaction_type, amount, description, created_at
        FROM transactions
    """
    params = ()
    if account_id is not None:
        query += " WHERE account_id = ?"
        params = (account_id,)
    query += " ORDER BY transaction_id DESC LIMIT 30"
    with connect() as conn:
        return conn.execute(query, params).fetchall()

def get_balance(account_id):
    with connect() as conn:
        row = conn.execute(
            "SELECT balance FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
    if row is None:
        raise ValueError("Account not found.")
    return row[0]

def record_transaction(conn, account_id, kind, amount, description):
    conn.execute(
        """INSERT INTO transactions(account_id, transaction_type, amount, description, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (account_id, kind, amount, description, datetime.now().isoformat(timespec="seconds"))
    )

def deposit(account_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    with connect() as conn:
        cur = conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
            (amount, account_id)
        )
        if cur.rowcount == 0:
            raise ValueError("Account not found.")
        record_transaction(conn, account_id, "Deposit", amount, "Cash deposit (demo)")
    return get_balance(account_id)

def withdraw(account_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    with connect() as conn:
        row = conn.execute(
            "SELECT balance FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        if row is None:
            raise ValueError("Account not found.")
        if amount > row[0]:
            raise ValueError("Insufficient balance.")
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE account_id = ?",
            (amount, account_id)
        )
        record_transaction(conn, account_id, "Withdrawal", amount, "Cash withdrawal (demo)")
    return get_balance(account_id)

def transfer(from_account, to_account, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if from_account == to_account:
        raise ValueError("Choose two different accounts.")
    with connect() as conn:
        sender = conn.execute(
            "SELECT balance FROM accounts WHERE account_id = ?", (from_account,)
        ).fetchone()
        receiver = conn.execute(
            "SELECT account_id FROM accounts WHERE account_id = ?", (to_account,)
        ).fetchone()
        if sender is None or receiver is None:
            raise ValueError("Sender or receiver account not found.")
        if amount > sender[0]:
            raise ValueError("Insufficient balance.")
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amount, from_account))
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (amount, to_account))
        record_transaction(conn, from_account, "Transfer Out", amount, f"Transfer to account {to_account}")
        record_transaction(conn, to_account, "Transfer In", amount, f"Transfer from account {from_account}")
    return get_balance(from_account), get_balance(to_account)

def ask_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a whole number.")

def ask_amount(prompt):
    try:
        value = float(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a valid amount, for example 500 or 125.50.")
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(value, 2)

def main():
    initialize_database()
    while True:
        print("\\n=== BANKING MANAGEMENT SYSTEM (DEMO) ===")
        print("1. View all accounts")
        print("2. Check account balance")
        print("3. Deposit money")
        print("4. Withdraw money")
        print("5. Transfer between demo accounts")
        print("6. View recent transactions")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                for account_id, name, kind, balance in list_accounts():
                    print(f"Account {account_id} | {name} | {kind} | Balance: ₹{balance:,.2f}")
            elif choice == "2":
                account_id = ask_int("Account ID (try 2001): ")
                print(f"Balance: ₹{get_balance(account_id):,.2f}")
            elif choice == "3":
                account_id = ask_int("Account ID (try 2001): ")
                amount = ask_amount("Deposit amount: ₹")
                print(f"Deposit complete. New balance: ₹{deposit(account_id, amount):,.2f}")
            elif choice == "4":
                account_id = ask_int("Account ID (try 2001): ")
                amount = ask_amount("Withdrawal amount: ₹")
                print(f"Withdrawal complete. New balance: ₹{withdraw(account_id, amount):,.2f}")
            elif choice == "5":
                sender = ask_int("From account ID (try 2001): ")
                receiver = ask_int("To account ID (try 2002): ")
                amount = ask_amount("Transfer amount: ₹")
                sender_balance, receiver_balance = transfer(sender, receiver, amount)
                print(f"Transfer complete. Sender balance: ₹{sender_balance:,.2f}; receiver balance: ₹{receiver_balance:,.2f}")
            elif choice == "6":
                account_text = input("Account ID, or press Enter for all accounts: ").strip()
                account_id = int(account_text) if account_text else None
                transactions = list_transactions(account_id)
                if not transactions:
                    print("No transactions found yet.")
                for row in transactions:
                    print(row)
            elif choice == "0":
                print("Goodbye. This was a local demo.")
                break
            else:
                print("Please choose one of the listed options.")
        except (ValueError, sqlite3.Error) as error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()
