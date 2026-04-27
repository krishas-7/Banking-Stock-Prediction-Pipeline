# ============================================================
# Banking Stock Prediction Pipeline — Dagster Orchestration
# Author: Krisha Shah
# ============================================================

from dagster import op, job, get_dagster_logger
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


@op
def fetch_data():
    logger = get_dagster_logger()
    data = yf.download("HDFCBANK.NS", start="2020-01-01", end="2024-01-01")
    data.reset_index(inplace=True)
    # Flatten multi-level columns from yfinance
    data.columns = [c[0] if isinstance(c, tuple) else c for c in data.columns]
    logger.info(f"Fetched {len(data)} rows of HDFC Bank stock data")
    return data


@op
def eda(data: pd.DataFrame):
    logger = get_dagster_logger()

    plt.figure(figsize=(10, 4))
    plt.plot(data["Date"], data["Close"])
    plt.title("HDFC Bank Close Price (2020–2024)")
    plt.xlabel("Date")
    plt.ylabel("Close Price (INR)")
    plt.tight_layout()
    plt.savefig("hdfc_close_price.png", dpi=150)
    plt.show()

    sns.histplot(data["Close"], kde=True)
    plt.title("Close Price Distribution")
    plt.tight_layout()
    plt.savefig("hdfc_distribution.png", dpi=150)
    plt.show()

    logger.info("EDA complete")
    return data


@op
def feature_engineering(data: pd.DataFrame):
    logger = get_dagster_logger()

    # Target: did price go UP the NEXT day?
    data["Return"] = data["Close"].pct_change()
    data["Target"] = (data["Return"] > 0).astype(int)

    # FIX: shift features by 1 so model uses YESTERDAY's data to predict TODAY
    # Avoids look-ahead leakage from using same-day Close as a feature
    feature_cols = ["Open", "High", "Low", "Close", "Volume"]
    X = data[feature_cols].shift(1)
    y = data["Target"]

    # Drop NaN rows created by shift
    combined = pd.concat([X, y], axis=1).dropna()
    X = combined[feature_cols]
    y = combined["Target"]

    logger.info(f"Features shape: {X.shape} | Target balance: {y.value_counts().to_dict()}")
    return train_test_split(X, y, test_size=0.2, random_state=42)


@op
def decision_tree(split_data):
    X_train, X_test, y_train, y_test = split_data
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Decision Tree Accuracy: {acc:.4f}")
    print(classification_report(y_test, model.predict(X_test)))
    return acc


@op
def knn(split_data):
    X_train, X_test, y_train, y_test = split_data
    model = KNeighborsClassifier()
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"KNN Accuracy: {acc:.4f}")
    print(classification_report(y_test, model.predict(X_test)))
    return acc


@op
def logistic_regression(split_data):
    X_train, X_test, y_train, y_test = split_data
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Logistic Regression Accuracy: {acc:.4f}")
    print(classification_report(y_test, model.predict(X_test)))
    return acc


@op
def random_forest(split_data):
    X_train, X_test, y_train, y_test = split_data
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Random Forest Accuracy: {acc:.4f}")
    print(classification_report(y_test, model.predict(X_test)))
    return acc


@job
def stock_ml_pipeline():
    data = fetch_data()
    eda_data = eda(data)
    split = feature_engineering(eda_data)

    decision_tree(split)
    knn(split)
    logistic_regression(split)
    random_forest(split)


if __name__ == "__main__":
    start = time.time()
    stock_ml_pipeline.execute_in_process()
    end = time.time()
    print(f"\nTotal Runtime WITH Dagster: {round(end - start, 2)} seconds")