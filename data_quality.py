import pandas as pd
import numpy as np

# ----------------------------
# LOAD DATA
# ----------------------------
def load_data():

    clients = pd.read_csv("data/clients.csv")
    accounts = pd.read_csv("data/accounts.csv")
    transactions = pd.read_csv("data/transactions.csv")

    return clients, accounts, transactions


# ----------------------------
# DATA QUALITY CHECKS
# ----------------------------
def check_missing_values(df):
    return df.isnull().sum().sum()


def check_duplicates(df):
    return df.duplicated().sum()


def check_negative_age(clients):
    return (clients["age"] < 0).sum()


def check_invalid_income(clients):
    return (clients["income"] < 0).sum()


def check_negative_balance(accounts):
    return (accounts["balance"] < -20000).sum()


def check_large_transactions(transactions):
    return (transactions["amount"].abs() > 1500).sum()


# ----------------------------
# QUALITY SCORE
# ----------------------------
def compute_quality_score(clients, accounts, transactions):

    issues = 0
    total_checks = 6

    issues += check_missing_values(clients)
    issues += check_missing_values(accounts)
    issues += check_missing_values(transactions)

    issues += check_duplicates(clients)
    issues += check_duplicates(accounts)
    issues += check_duplicates(transactions)

    issues += check_negative_age(clients)
    issues += check_invalid_income(clients)
    issues += check_negative_balance(accounts)
    issues += check_large_transactions(transactions)

    score = max(0, 100 - issues)

    return score, issues


# ----------------------------
# SUMMARY REPORT
# ----------------------------
def generate_quality_report():

    clients, accounts, transactions = load_data()

    score, issues = compute_quality_score(clients, accounts, transactions)

    report = {
        "quality_score": score,
        "total_issues": issues,
        "clients_rows": len(clients),
        "accounts_rows": len(accounts),
        "transactions_rows": len(transactions)
    }

    return report


if __name__ == "__main__":

    report = generate_quality_report()
    print(report)