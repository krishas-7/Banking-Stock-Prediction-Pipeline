# 🏦 Banking Stock Prediction Pipeline

> End-to-end ML pipeline for HDFC Bank stock trend prediction — orchestrated with Dagster for **60% faster execution**.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Dagster](https://img.shields.io/badge/Dagster-5E4FF6?style=flat-square&logo=dagster&logoColor=white)
![ML](https://img.shields.io/badge/Machine_Learning-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

---

## 📌 Project Overview

This project demonstrates how integrating **DevOps principles (pipeline orchestration)** into a data science workflow dramatically improves execution efficiency. The pipeline predicts HDFC Bank stock trends using historical data and multiple ML models.

**Key Result:** Execution time reduced from **~5 minutes → ~2 minutes** (60% improvement) by replacing manual Jupyter notebook runs with Dagster's dependency-aware execution.

---

## 🔍 Problem Statement

Traditional ML workflows in Jupyter notebooks require re-running the **entire pipeline** whenever data or parameters change — leading to redundancy and wasted compute time. This project solves that with modular, orchestrated pipeline stages.

---

## ⚙️ Pipeline Stages

```
Data Collection → EDA → Feature Engineering → Data Splitting → Model Training → Evaluation
```

Each stage is an independent Dagster **op** — only affected stages re-run on changes.

---

## 🤖 Models Used

| Model | Type |
|---|---|
| Decision Tree | Classification |
| Random Forest | Ensemble |
| Logistic Regression | Classification |
| K-Nearest Neighbors | Instance-based |

---

## 📊 Evaluation Metrics

- Accuracy
- Precision & Recall
- F1-Score
- Confusion Matrix

---

## 🗂️ Project Structure

```
banking-stock-prediction-pipeline/
│
├── data/
│   └── hdfc_stock_data.csv        # Historical stock data
│
├── pipeline/
│   ├── data_collection.py         # Dagster op: fetch data
│   ├── eda.py                     # Dagster op: exploratory analysis
│   ├── feature_engineering.py     # Dagster op: create features
│   ├── model_training.py          # Dagster op: train models
│   └── evaluation.py              # Dagster op: evaluate & compare
│
├── notebooks/
│   └── exploration.ipynb          # Initial Jupyter exploration
│
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/krishas-7/banking-stock-prediction-pipeline.git
cd banking-stock-prediction-pipeline

# Install dependencies
pip install -r requirements.txt

# Launch Dagster UI
dagster dev

# Open http://localhost:3000 and trigger the pipeline
```

---

## 📈 Results

| Execution Mode | Time |
|---|---|
| Traditional (full notebook run) | ~5 minutes |
| Dagster (selective re-execution) | ~2 minutes |
| **Improvement** | **60% faster** |

---

## 🔗 Related

- [Smart Farming – Irrigation Prediction](https://github.com/krishas-7/smart-farming-irrigation-prediction)

---

*Built by [Krisha Shah](https://www.linkedin.com/in/krishas7) · Mumbai, India*
