# 🏦 CA Data Vision — Data Governance & Risk Intelligence Platform

## 📌 Présentation

CA Data Vision est une plateforme de **Data Governance, Data Engineering et Data Science** simulant un **Data Office bancaire**.

Le projet reproduit un environnement réel utilisé dans les banques pour :
- contrôler la qualité des données
- analyser les clients et transactions
- détecter des anomalies financières
- gérer le risque client
- automatiser le reporting et les alertes

---

## 🎯 Objectifs

- Simuler une architecture Data Office bancaire end-to-end
- Fiabiliser et analyser des données financières
- Détecter des comportements suspects (fraude / anomalies)
- Construire un système de reporting automatisé
- Centraliser la donnée dans une architecture simple mais réaliste

---

## 🏗️ Architecture du projet
Génération de données (Faker)
↓
Stockage (SQLite / Pandas CSV)
↓
API (FastAPI)
↓
Dashboard (Streamlit)
↓
Data Quality + Machine Learning
↓
Alerting Email (SMTP Gmail)

---

## ⚙️ Stack technique

- Python 3
- Pandas / NumPy
- Faker (génération de données)
- SQLite (stockage local)
- Streamlit (dashboard interactif)
- FastAPI (API REST)
- Plotly (visualisations)
- Scikit-learn (anomaly detection)
- SMTP (email alerting)

---

## 📊 Fonctionnalités

### ✔ Data Engineering
- Génération de données clients, comptes et transactions
- Structuration des données bancaires simulées
- Stockage en base SQLite

---

### ✔ Data Quality (Data Governance)
- Score global de qualité des données
- Détection de valeurs manquantes et incohérences
- Reporting automatisé

---

### ✔ Data Visualization
- Analyse des clients (âge, revenus)
- Analyse des comptes bancaires
- Analyse des transactions
- Visualisation des outliers

---

### ✔ Machine Learning
- Détection d’anomalies avec Isolation Forest
- Identification de transactions suspectes
- Scoring de risque client

---

### ✔ Data Governance / Reporting
- Génération de rapports automatisés
- Data Catalog (inventaire des données)
- Tableaux de bord Data Office

---

### ✔ Alerting System
- Envoi automatique d’emails en cas d’anomalies
- Rapport détaillé des transactions suspectes
- Simulation de monitoring bancaire

---

## 📡 API (FastAPI)

Endpoints disponibles :

- `/` → statut API
- `/clients` → liste des clients
- `/transactions` → liste des transactions

---

## 📊 Dashboard

Lancer le dashboard :

```bash
streamlit run app/dashboard.py