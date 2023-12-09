from transformers import pipeline
from dotenv import load_dotenv
import os
from databricks import sql
from collections import Counter
import pandas as pd
import plotly.express as px

load_dotenv()
pipe = pipeline("text-classification")

# connect to our databricks
DATABRICKS = os.getenv("DATABRICKS")
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")


def fetch_news():
    """Fetch all rows of dataset of news"""
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
        return result


def create_news_df():
    """Create Pandas Dataframe with Daily Sentiment Totals and Analysis"""
    data = fetch_news()
    data_list = [
        {
            "Date": row.date,
            "Source": row.source,
            "Text": row.text,
        }
        for row in data
    ]
    df = pd.DataFrame(data_list)

    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sentiment"] = df["Text"].apply(lambda x: pipe(x))
    df["Sentiment"] = df["Sentiment"].apply(lambda x: x[0]["label"])
    unique_dates = df["Date"].unique()

    # Create a new DataFrame with the desired structure
    result_data = {"Date": unique_dates, "Positive": [], "Negative": []}

    # Count the occurrences of 'Positive' and 'Negative' for each unique date
    for date in unique_dates:
        sentiment_counts = Counter(df[df["Date"] == date]["Sentiment"])
        result_data["Positive"].append(sentiment_counts.get("POSITIVE", 0))
        result_data["Negative"].append(sentiment_counts.get("NEGATIVE", 0))

    result_df = pd.DataFrame(result_data)

    # Calculate cumulative sums for 'Positive' and 'Negative'
    result_df["Cumulative_Positive"] = result_df["Positive"].cumsum()
    result_df["Cumulative_Negative"] = result_df["Negative"].cumsum()

    result_df["Pos-Neg"] = result_df["Positive"] - result_df["Negative"]

    result_df["Cumulative_Difference"] = result_df["Pos-Neg"].cumsum()

    # Calculate the ratio of cumulative positive to the sum of cumulative positive and cumulative negative
    result_df["Cumulative_Positive_Ratio"] = result_df["Cumulative_Positive"] / (
        result_df["Cumulative_Positive"] + result_df["Cumulative_Negative"]
    )
    return result_df


"""Functions to Create Visualizations
set news = create_news_df(), and then input news as data"""


def News_Cumulative_Diff_Graph(data):
    fig = px.line(
        data,
        x="Date",
        y="Cumulative_Difference",
        labels={"value": "Percentage", "variable": "Sentiment"},
        title="Cumulative Positive - Negative Sentiment Over Time",
    )
    fig.write_html("static/cumulative_news_data.html")


def News_Cumulative_Ratio_Graph(data):
    fig = px.line(
        data,
        x="Date",
        y="Cumulative_Positive_Ratio",
        labels={"value": "Percentage", "variable": "Sentiment"},
        title="Cumulative Positive Sentiment Ratio Over Time",
    )
    return fig


def News_Bars_Graph(data):
    result_df_melted = pd.melt(
        data,
        id_vars=["Date"],
        value_vars=["Positive", "Negative"],
        var_name="Sentiment",
        value_name="Count",
    )

    # Create a grouped bar chart using Plotly Express
    fig = px.bar(
        result_df_melted,
        x="Date",
        y="Count",
        color="Sentiment",
        barmode="group",
        labels={"Count": "Sentiment percentages", "Date": "Date"},
        title="Positive and Negative Sentiment Percentages Over Time",
    )
    return fig
