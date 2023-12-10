from technical_indicators import (
    add_technical_indicators,
    flatten_byDatetime,
    long_df,
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from databricks import sql

load_dotenv()
# connect to our databricks
DATABRICKS = os.getenv("DATABRICKS")
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")


def fetch_all_stocks():
    """Fetch the entire dataset of news"""
    server_h = DATABRICKS_HOST
    access_token = DATABRICKS
    http_path = DATABRICKS_PATH
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute("SELECT * FROM default.stock;")
        result = c.fetchall()
        c.close()

        return result


def fetch_all_news():
    """Fetch the entire dataset of news"""
    server_h = DATABRICKS_HOST
    access_token = DATABRICKS
    http_path = DATABRICKS_PATH
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute("SELECT * FROM default.news;")
        result = c.fetchall()
        c.close()

        return result


def import_prep():
    """import data, add technical indicators + labels, return flattened df"""
    data = fetch_all_stocks()

    data_list = [
        {
            "Date": row.Date,
            "Price_type": row.Price_type,
            "Instrument": row.Instrument,
            "Price": row.Price,
        }
        for row in data
    ]
    stocks = pd.DataFrame(data_list)
    stocks = long_df(stocks)
    stocks = add_technical_indicators(stocks)
    stocks = stocks.drop(
        columns=["Adj Close", "Close", "Open", "High", "Low", "Volume"]
    )
    flattened_stocks = flatten_byDatetime(stocks)
    return flattened_stocks


def ml_prep(flattened_df, ticker, days=13):
    assert days in [1, 5, 8, 13], "days must be 1, 5, 8, or 13"
    assert f"label_{days}d_{ticker}" in flattened_df.columns, "ticker not found"
    flattened_df.dropna(inplace=True)
    # define target variable and create y_true
    target_variable = f"label_{days}d_{ticker}"
    y_true = flattened_df[target_variable]
    y_true = y_true.iloc[days:]
    # define features
    X = flattened_df.drop(columns=["Datetime"])
    X = X.shift(days)
    X.dropna(inplace=True)
    return X, y_true


def random_forest_classifier(X, y, test_size=0.2, max_depth=10, random_state=257):
    """Random Forest Classifier"""

    # split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # train model
    clf = RandomForestClassifier(
        n_estimators=100, max_depth=max_depth, random_state=random_state
    )
    clf.fit(X_train, y_train)

    # predict on test data
    y_pred = clf.predict(X_test)

    # evaluate model
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    # Generate the confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Plot the confusion matrix
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Truth")
    plt.show()

    return clf
