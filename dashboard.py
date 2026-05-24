import streamlit as st
import pandas as pd
import plotly.express as px

from data_quality import generate_quality_report
from anomaly_detection import run_anomaly_detection
from utils import export_report
from email_alert import send_alert_email, build_anomaly_report
from data_catalog import generate_catalog
from risk_scoring import compute_risk_score
from auth import login, is_authenticated
# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(
    page_title="CA Data Vision",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------
# 🎨 CREDIT AGRICOLE THEME PRO
# ----------------------------
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background-color: #ffffff;
    color: #1a1a1a;
}

/* TITRES */
h1, h2, h3, h4 {
    color: #0b6e4f !important;
    font-weight: 700;
}

/* TEXTES */
p, span, div, label {
    color: #1a1a1a !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #0b6e4f;
    color: white;
}

/* BUTTONS */
.stButton>button {
    background-color: #0b6e4f;
    color: white !important;
    border-radius: 8px;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #095c41;
}

/* INPUT */
input {
    color: #1a1a1a !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background-color: #f7f7f2;
    border-left: 5px solid #0b6e4f;
    padding: 12px;
    border-radius: 10px;
}

/* TABLE VISUAL ONLY */
div[data-testid="stDataFrame"] {
    background-color: #f7f7f2 !important;
    border: 1px solid #0b6e4f !important;
    border-radius: 10px;
}

div[data-testid="stDataFrame"] * {
    color: #0b6e4f !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🔥 FIX TABLE STYLE (IMPORTANT)
# ----------------------------
def style_df(df):
    return df.style.set_properties(
        **{
            "background-color": "#f7f7f2",
            "color": "#0b6e4f",
            "border-color": "#cfe5d9"
        }
    )

# ----------------------------
# AUTH
# ----------------------------
if not is_authenticated():
    login()
    st.stop()

# ----------------------------
# HEADER
# ----------------------------
st.title("🏦 Crédit Agricole - Data Vision")
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
# DATA QUALITY
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
# REPORTING
# ----------------------------
st.markdown("## 📄 Data Governance Report")

if st.button("📥 Générer un rapport Data Office"):
    file_path = export_report()
    st.success("Rapport généré ✔")
    st.write(file_path)

st.divider()

# ----------------------------
# CLIENTS
# ----------------------------
st.markdown("## 👥 Clients Analysis")

fig1 = px.histogram(clients, x="age", title="Âge des clients",
                    color_discrete_sequence=["#0b6e4f"])
fig1.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(clients, x="income", title="Revenus des clients",
                    color_discrete_sequence=["#0b6e4f"])
fig2.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# ACCOUNTS
# ----------------------------
st.markdown("## 🏦 Accounts Analysis")

fig3 = px.histogram(accounts, x="balance", title="Soldes des comptes",
                    color_discrete_sequence=["#0b6e4f"])
fig3.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.box(accounts, y="balance", title="Outliers des soldes",
              color_discrete_sequence=["#0b6e4f"])
fig4.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# TRANSACTIONS
# ----------------------------
st.markdown("## 💳 Transactions Analysis")

fig5 = px.histogram(transactions, x="amount", nbins=50,
                    title="Transactions",
                    color_discrete_sequence=["#0b6e4f"])
fig5.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")
st.plotly_chart(fig5, use_container_width=True)

fig6 = px.box(transactions, y="amount", title="Outliers transactions",
              color_discrete_sequence=["#0b6e4f"])
fig6.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")
st.plotly_chart(fig6, use_container_width=True)

# ----------------------------
# ANOMALIES
# ----------------------------
st.markdown("## ⚠ Anomalies Detection")

st.dataframe(style_df(anomalies_df[anomalies_df["is_anomaly"] == 1]),
             use_container_width=True)

# ----------------------------
# CATALOG
# ----------------------------
st.markdown("## 📚 Data Catalog")

st.dataframe(style_df(generate_catalog()), use_container_width=True)

# ----------------------------
# RAW DATA
# ----------------------------
st.markdown("## 📁 Raw Data")

tab1, tab2, tab3 = st.tabs(["Clients", "Accounts", "Transactions"])

with tab1:
    st.dataframe(style_df(clients), use_container_width=True)

with tab2:
    st.dataframe(style_df(accounts), use_container_width=True)

with tab3:
    st.dataframe(style_df(transactions), use_container_width=True)

# ----------------------------
# RISK
# ----------------------------
st.markdown("## ⚠ Risk Scoring")

clients_risk = compute_risk_score(clients)

fig_risk = px.histogram(clients_risk, x="risk_score",
                        color_discrete_sequence=["#0b6e4f"])
fig_risk.update_layout(plot_bgcolor="#f7f7f2", paper_bgcolor="#f7f7f2")

st.plotly_chart(fig_risk, use_container_width=True)

st.dataframe(
    style_df(clients_risk.sort_values("risk_score", ascending=False)),
    use_container_width=True
)

# ----------------------------
# EMAIL ALERT (FULL DETAILS FIX)
# ----------------------------
if int(anomalies_df["is_anomaly"].sum()) > 50:

    anomalies_only = anomalies_df[anomalies_df["is_anomaly"] == 1]

    # limiter si énorme dataset (sécurité email)
    preview = anomalies_only.head(50)

    email_message = f"""
🚨 CA DATA VISION - ALERTES ANOMALIES

=========================
📊 RESUME
=========================
- Nombre total d'anomalies : {len(anomalies_only)}
- Score qualité : {report['quality_score']}

=========================
📌 DETAILS DES ANOMALIES
=========================

{preview.to_string(index=False)}

=========================
⚠ NOTE
=========================
Les 50 premières anomalies sont affichées.
Vérification complète recommandée via dashboard.
"""

    send_alert_email(
        subject="CA Data Vision - Alertes anomalies (DETAILS COMPLETS)",
        message=email_message
    )
# ----------------------------
# EMAIL BUTTON
# ----------------------------
if st.button("📧 Envoyer rapport email"):
    email_content = build_anomaly_report(anomalies_df, report)

    send_alert_email(
        subject="CA Data Vision - Rapport",
        message=email_content
    )

    st.success("Email envoyé ✔")