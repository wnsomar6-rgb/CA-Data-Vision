import pandas as pd

# ----------------------------
# DATA CATALOG (META DATA)
# ----------------------------
def generate_catalog():

    catalog = pd.DataFrame([
        {
            "table": "clients",
            "description": "Informations clients de la banque",
            "columns": "client_id, name, age, income, risk_profile"
        },
        {
            "table": "accounts",
            "description": "Comptes bancaires des clients",
            "columns": "account_id, client_id, balance, account_type"
        },
        {
            "table": "transactions",
            "description": "Transactions financières clients",
            "columns": "transaction_id, account_id, amount, date, transaction_type"
        }
    ])

    return catalog


if __name__ == "__main__":
    print(generate_catalog())