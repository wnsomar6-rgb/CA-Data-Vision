import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# ----------------------------
# LOAD DATA
# ----------------------------
def load_transactions():

    df = pd.read_csv("data/transactions.csv")
    return df


# ----------------------------
# FEATURE ENGINEERING
# ----------------------------
def prepare_data(df):

    data = df.copy()

    # transformer la date
    data["date"] = pd.to_datetime(data["date"])
    data["hour"] = data["date"].dt.hour
    data["day"] = data["date"].dt.day
    data["month"] = data["date"].dt.month

    # valeur absolue transaction
    data["abs_amount"] = data["amount"].abs()

    return data


# ----------------------------
# MODEL TRAINING
# ----------------------------
def detect_anomalies(df):

    features = df[["abs_amount", "hour", "day", "month"]]

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df["anomaly_score"] = model.fit_predict(features)

    # -1 = anomalie, 1 = normal
    df["is_anomaly"] = df["anomaly_score"].apply(lambda x: 1 if x == -1 else 0)

    return df


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def run_anomaly_detection():

    df = load_transactions()
    df = prepare_data(df)
    df = detect_anomalies(df)

    return df


if __name__ == "__main__":

    result = run_anomaly_detection()

    print("Anomalies détectées :", result["is_anomaly"].sum())
    print(result.head())