import pandas as pd
from datetime import datetime
import os

from data_quality import generate_quality_report
from anomaly_detection import run_anomaly_detection

# ----------------------------
# CREATE REPORT DIRECTORY
# ----------------------------
def ensure_dir():

    if not os.path.exists("generated_reports"):
        os.makedirs("generated_reports")


# ----------------------------
# GENERATE DATA SUMMARY
# ----------------------------
def generate_summary():

    report = generate_quality_report()
    anomalies_df = run_anomaly_detection()

    summary = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "quality_score": report["quality_score"],
        "total_issues": report["total_issues"],
        "transactions": report["transactions_rows"],
        "anomalies_detected": int(anomalies_df["is_anomaly"].sum())
    }

    return summary


# ----------------------------
# EXPORT REPORT (CSV)
# ----------------------------
def export_report():

    ensure_dir()

    summary = generate_summary()

    df = pd.DataFrame([summary])

    file_path = f"generated_reports/data_governance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    df.to_csv(file_path, index=False)

    return file_path