import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

from app.database import save_to_db

fake = Faker()

# ----------------------------
# CONFIG
# ----------------------------
NUM_CLIENTS = 200
NUM_ACCOUNTS = 300
NUM_TRANSACTIONS = 2000

# ----------------------------
# CLIENTS
# ----------------------------
def generate_clients():
    clients = []

    for i in range(NUM_CLIENTS):
        clients.append({
            "client_id": i + 1,
            "name": fake.name(),
            "age": random.randint(18, 85),
            "country": "France",
            "income": random.randint(12000, 120000),
            "risk_profile": random.choice(["low", "medium", "high"])
        })

    return pd.DataFrame(clients)

# ----------------------------
# ACCOUNTS
# ----------------------------
def generate_accounts(clients_df):
    accounts = []

    for i in range(NUM_ACCOUNTS):
        client_id = random.choice(clients_df["client_id"].tolist())

        accounts.append({
            "account_id": i + 1,
            "client_id": client_id,
            "balance": round(random.uniform(-5000, 50000), 2),
            "account_type": random.choice(["checking", "savings"])
        })

    return pd.DataFrame(accounts)

# ----------------------------
# TRANSACTIONS
# ----------------------------
def generate_transactions(accounts_df):
    transactions = []

    for i in range(NUM_TRANSACTIONS):
        account_id = random.choice(accounts_df["account_id"].tolist())

        date = datetime.now() - timedelta(days=random.randint(0, 365))

        transactions.append({
            "transaction_id": i + 1,
            "account_id": account_id,
            "amount": round(random.uniform(-2000, 2000), 2),
            "transaction_type": random.choice(["payment", "transfer", "withdrawal"]),
            "date": date
        })

    return pd.DataFrame(transactions)

# ----------------------------
# MAIN PIPELINE
# ----------------------------
def generate_all_data():

    clients = generate_clients()
    accounts = generate_accounts(clients)
    transactions = generate_transactions(accounts)

    return clients, accounts, transactions


if __name__ == "__main__":

    clients, accounts, transactions = generate_all_data()

    # CSV export
    clients.to_csv("data/clients.csv", index=False)
    accounts.to_csv("data/accounts.csv", index=False)
    transactions.to_csv("data/transactions.csv", index=False)

    # DB export
    save_to_db(clients, accounts, transactions)

    print("Data generated + saved to DB ✔")