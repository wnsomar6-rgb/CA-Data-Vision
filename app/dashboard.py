import streamlit as st
import pandas as pd
import plotly.express as px

from data_quality import generate_quality_report
from anomaly_detection import run_anomaly_detection
from utils import export_report
from email_alert import send_alert_email, build_anomaly_report
# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(
    page_title="CA Data Vision",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 CA Data Vision")
st.subheader("Data Governance & Risk Intelligence Platform")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():

    clients = pd.read_csv("data/clients.csv")
    accounts = pd.read_csv("data/accounts.csv")
    transactions = pd.read_csv("data/transactions.csv")

    return clients, accounts, transactions


clients, accounts, transactions = load_data()

# ----------------------------
# DATA QUALITY + ANOMALIES
# ----------------------------
report = generate_quality_report()
anomalies_df = run_anomaly_detection()

st.markdown("## 📊 Data Governance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Quality Score", f"{report['quality_score']} / 100")
col2.metric("Total Issues", report["total_issues"])
col3.metric("Transactions", report["transactions_rows"])
col4.metric("Anomalies", int(anomalies_df["is_anomaly"].sum()))

st.divider()

# ----------------------------
# REPORTING DATA OFFICE
# ----------------------------
st.markdown("## 📄 Data Governance Report (Data Office)")

if st.button("📥 Générer un rapport Data Office"):

    file_path = export_report()

    st.success("Rapport généré avec succès ✔")
    st.write(f"Fichier exporté : {file_path}")

st.divider()

# ----------------------------
# CLIENT ANALYSIS
# ----------------------------
st.markdown("## 👥 Clients Analysis")

fig1 = px.histogram(
    clients,
    x="age",
    title="Distribution des âges des clients"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(
    clients,
    x="income",
    title="Distribution des revenus des clients"
)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# ACCOUNTS ANALYSIS
# ----------------------------
st.markdown("## 🏦 Accounts Analysis")

fig3 = px.histogram(
    accounts,
    x="balance",
    title="Distribution des soldes de comptes"
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.box(
    accounts,
    y="balance",
    title="Analyse des outliers des soldes"
)
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# TRANSACTIONS ANALYSIS
# ----------------------------
st.markdown("## 💳 Transactions Analysis")

fig5 = px.histogram(
    transactions,
    x="amount",
    nbins=50,
    title="Distribution des transactions"
)
st.plotly_chart(fig5, use_container_width=True)

fig6 = px.box(
    transactions,
    y="amount",
    title="Outliers des transactions"
)
st.plotly_chart(fig6, use_container_width=True)

# ----------------------------
# ANOMALIES SECTION (ML)
# ----------------------------
st.markdown("## ⚠ Anomalies Detection (Machine Learning)")

anomalies_only = anomalies_df[anomalies_df["is_anomaly"] == 1]

st.write("Transactions suspectes détectées automatiquement :")
st.dataframe(anomalies_only)

# ----------------------------
# DATA CATALOG SECTION
# ----------------------------
st.markdown("## 📚 Data Catalog (Governance)")

from data_catalog import generate_catalog

catalog = generate_catalog()

st.dataframe(catalog)

# ----------------------------
# RAW DATA VIEW
# ----------------------------
st.markdown("## 📁 Data Catalog / Raw Data")

tab1, tab2, tab3 = st.tabs(["Clients", "Accounts", "Transactions"])

with tab1:
    st.dataframe(clients)

with tab2:
    st.dataframe(accounts)

with tab3:
    st.dataframe(transactions)

# ----------------------------
# RISK ANALYSIS
# ----------------------------
from risk_scoring import compute_risk_score

st.markdown("## ⚠ Client Risk Scoring")

clients_risk = compute_risk_score(clients)

fig_risk = px.histogram(
    clients_risk,
    x="risk_score",
    title="Distribution des scores de risque clients"
)

st.plotly_chart(fig_risk, use_container_width=True)

st.dataframe(clients_risk.sort_values("risk_score", ascending=False))

# ----------------------------
# EMAIL ALERT LOGIC
# ----------------------------
if int(anomalies_df["is_anomaly"].sum()) > 50:

    send_alert_email(
        subject="CA Data Vision - Alertes anomalies",
        message=f"""
Attention !

Trop d'anomalies détectées dans le système :
- Anomalies: {int(anomalies_df['is_anomaly'].sum())}

Vérification requise du Data Office.
"""
    )

# ----------------------------
# EMAIL BUTTON (CORRIGÉ)
# ----------------------------
if st.button("📧 Envoyer rapport par email"):

    email_content = build_anomaly_report(anomalies_df, report)

    send_alert_email(
        subject="CA Data Vision - Rapport Anomalies Data Office",
        message=email_content
    )

    st.success("Email envoyé avec anomalies détaillées ✔")