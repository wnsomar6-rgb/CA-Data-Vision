import pandas as pd

# ----------------------------
# SIMPLE RISK SCORING MODEL
# ----------------------------
def compute_risk_score(clients_df):

    df = clients_df.copy()

    def score(row):

        score = 0

        # âge
        if row["age"] < 25:
            score += 30
        elif row["age"] > 65:
            score += 20

        # revenu
        if row["income"] < 20000:
            score += 40
        elif row["income"] < 40000:
            score += 20

        # risk profile
        if row["risk_profile"] == "high":
            score += 40
        elif row["risk_profile"] == "medium":
            score += 20

        return score

    df["risk_score"] = df.apply(score, axis=1)

    return df


if __name__ == "__main__":
    print("Risk module ready")