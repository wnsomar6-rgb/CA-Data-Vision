import smtplib
from email.mime.text import MIMEText
import pandas as pd

# ----------------------------
# CONFIG EMAIL
# ----------------------------
EMAIL_SENDER = "wnsomar6@gmail.com"
EMAIL_PASSWORD = "ejhs lqen srjk wbob"
EMAIL_RECEIVER = "wnsomar6@gmail.com"


# ----------------------------
# SEND EMAIL WITH ANOMALIES
# ----------------------------
def send_alert_email(subject, message):

    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print("Email sent ✔")

    except Exception as e:
        print("Email error:", e)


# ----------------------------
# FORMAT ANOMALIES REPORT
# ----------------------------
def build_anomaly_report(anomalies_df, report):

    anomalies_only = anomalies_df[anomalies_df["is_anomaly"] == 1]

    # limiter pour éviter email trop long
    top_anomalies = anomalies_only.head(20)

    message = f"""
📊 CA DATA VISION - DATA OFFICE ALERT

========================
📌 KPI GÉNÉRAUX
========================
- Quality Score: {report['quality_score']} / 100
- Total Issues: {report['total_issues']}
- Total Transactions: {report['transactions_rows']}
- Anomalies détectées: {len(anomalies_only)}

========================
⚠ TOP ANOMALIES
========================
"""

    if len(top_anomalies) == 0:
        message += "\nAucune anomalie détectée.\n"
    else:
        for _, row in top_anomalies.iterrows():
            message += f"""
- Transaction ID: {row.get('transaction_id', 'N/A')}
  Account ID: {row.get('account_id', 'N/A')}
  Amount: {row.get('amount', 'N/A')}
"""

    message += """

========================
🔎 ANALYSE
========================
Système de monitoring Data Office automatique.
Vérification recommandée des transactions suspectes.

CA Data Vision - Automated Report
"""

    return message