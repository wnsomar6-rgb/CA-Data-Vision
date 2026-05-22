from sqlalchemy import create_engine
import pandas as pd
import os

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
DB_PATH = "ca_data_vision.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


def save_to_db(clients, accounts, transactions):

    clients.to_sql("clients", engine, if_exists="replace", index=False)
    accounts.to_sql("accounts", engine, if_exists="replace", index=False)
    transactions.to_sql("transactions", engine, if_exists="replace", index=False)

    print("Data saved to database ✔")


def load_from_db():

    # ----------------------------
    # CHECK DB EXISTS
    # ----------------------------
    if not os.path.exists(DB_PATH):
        raise Exception("Database not found. Run data_generator.py first.")

    try:
        clients = pd.read_sql("clients", engine)
        accounts = pd.read_sql("accounts", engine)
        transactions = pd.read_sql("transactions", engine)

        return clients, accounts, transactions

    except Exception as e:
        raise Exception(f"Database error: {str(e)}")