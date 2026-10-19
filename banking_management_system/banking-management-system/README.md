# Banking Management System (Python + SQLite)

A beginner-friendly command-line banking simulation for practicing Python, SQL/SQLite, database relationships, validation, and transaction history.

> **Important:** This is an educational demo with fictional data. It is not a real banking system and must never be used to store real customer details or move real money. It has no login/authentication, authorization, encryption, audit-grade controls, or regulatory safeguards.

## Features
- View fictional customer accounts and balances
- Check an account balance
- Deposit and withdraw demo funds
- Transfer demo funds between two accounts
- Store transaction history with timestamps
- Use SQLite tables with primary keys, foreign keys, and basic constraints
- Reject invalid amounts, unknown accounts, same-account transfers, and withdrawals/transfers exceeding the balance

## Technologies
- Python 3
- SQLite (included with standard Python installation)

## Project structure
```text
banking-management-system/
├── banking_management.py
├── README.md
├── data/
│   ├── customers.csv
│   └── accounts.csv
└── outputs/
    └── (SQLite database is created locally when you run the program)
```

## Run on Windows
1. Install Python 3 from https://www.python.org/downloads/ if it is not already installed. During installation, select **Add Python to PATH**.
2. Extract the downloaded ZIP file.
3. Open the extracted `banking-management-system` folder in VS Code.
4. Choose **Terminal → New Terminal**.
5. Run:
   ```bash
   python banking_management.py
   ```
   If Windows does not recognize `python`, try:
   ```bash
   py banking_management.py
   ```

No third-party Python libraries are required.

## Try the demo
Choose option `1` to see the sample accounts. Example account IDs are `2001` through `2005`.
- Option `2`: check balance
- Option `3`: deposit a small test amount
- Option `4`: withdraw a test amount
- Option `5`: transfer between accounts, e.g. 2001 to 2002
- Option `6`: review transaction history
- Option `0`: exit

The program creates `banking.db` locally on first run. To reset the demo to its original sample balances, exit the program and delete `banking.db`; it will be recreated next time.

## Resume bullet (use after running and understanding it)
**Banking Management System | Python, SQLite**
- Built a command-line banking simulation to view accounts, check balances, deposit/withdraw demo funds, and transfer funds between accounts.
- Designed SQLite tables for customers, accounts, and transaction history using primary/foreign keys and basic validation constraints.
- Added checks for invalid amounts, missing accounts, insufficient funds, and same-account transfers.

## Limitations
This is a learning project only. It does not implement real banking security, user login, role-based access, encryption, fraud detection, or compliance controls. All names, emails, phone numbers, and balances are fictional.
