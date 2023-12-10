from dotenv import load_dotenv
import os
from flask import Flask, render_template, jsonify, request
from databricks import sql

# import openai
from datetime import datetime, timedelta
import pytz
import pandas as pd
import plotly.express as px
import numpy as np
from collections import Counter
import plotly.graph_objects as go

load_dotenv()

app = Flask(__name__, static_folder="static")

# Azure Databricks API token
DATABRICKS = os.getenv("DATABRICKS")
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")

# openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_news():
    """Fetch 5 rows of dataset of news"""
    server_h = DATABRICKS_HOST
    access_token = DATABRICKS
    http_path = DATABRICKS_PATH
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute("""
                  SELECT *
                  FROM default.news
                  ORDER BY RAND()
                  LIMIT 5;
                  """)
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


def get_stocks_for_week():
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
        for entry in result:
            entry_date = entry["Date"]
            if isinstance(entry_date, datetime):
                entry_date = entry_date.astimezone(pytz.timezone("UTC"))

        # Find the closest week range to today
        today = datetime.utcnow().replace(
            tzinfo=pytz.UTC
        )  # Make today an aware datetime
        days_back = 20
        duration = timedelta(days=days_back)  # Create a timedelta object for 20 days
        week_start = (
            today - duration
        )  # Subtract the timedelta from today to get the start of the week
        week_end = today

        # Filter data for the closest week
        closest_week_data = [
            entry
            for entry in result
            if week_start <= entry["Date"].astimezone(pytz.UTC) <= week_end
        ]
        return closest_week_data


def weekly_stocks_graph_spy(start_date, end_date, ticker):
    """Saves the graph as an HTML file, not just spy"""
    # converting the data to a pandas dataframe
    data = fetch_all_stocks()
    news_data = fetch_all_news()

    data_list = [
        {
            "Date": row.Date,
            "Price_type": row.Price_type,
            "Instrument": row.Instrument,
            "Price": row.Price,
        }
        for row in data
    ]

    news_data_list = [
        {
            "Date": row.date,
            "Source": row.source,
            "Text": row.text,
            "Sentiment": row.Sentiment
        }
        for row in news_data
    ]
    news_df = pd.DataFrame(news_data_list)

    # Convert Date column to datetime format
    news_df["Date"] = pd.to_datetime(news_df["Date"])
    unique_dates = news_df["Date"].unique()
    # Create a new DataFrame with the desired structure
    result_data = {"Date": unique_dates, "Positive": [], "Negative": []}

    # Count the occurrences of 'Positive' and 'Negative' for each unique date
    for date in unique_dates:
        sentiment_counts = Counter(news_df[news_df["Date"] == date]["Sentiment"])
        result_data["Positive"].append(sentiment_counts.get("POSITIVE", 0))
        result_data["Negative"].append(sentiment_counts.get("NEGATIVE", 0))

    result_df = pd.DataFrame(result_data)

    # Calculate cumulative sums for 'Positive' and 'Negative'
    result_df["Cumulative_Positive"] = result_df["Positive"].cumsum()
    result_df["Cumulative_Negative"] = result_df["Negative"].cumsum()

    result_df["Pos-Neg"] = result_df["Positive"] - result_df["Negative"]

    result_df["Cumulative_Difference"] = result_df["Pos-Neg"].cumsum()
    # update later lol
    if start_date < "2023-11-05":
        start_date = "2023-11-05"
    if end_date < "2023-11-05":
        end_date = "2023-11-11"

    result_df = result_df[(result_df["Date"] >= start_date) & 
                          (result_df["Date"] <= end_date)]
    
    result_df_melted = pd.melt(
        result_df,
        id_vars=["Date"],
        value_vars=["Positive", "Negative"],
        var_name="Sentiment",
        value_name="Count",
    )


    df = pd.DataFrame(data_list)

    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    df1 = df[df["Price_type"] == "Adj Close"]
    df1 = df1[df1["Instrument"] == ticker]
    df1 = df1[(df1["Date"] >= start_date) & (df1["Date"] <= end_date)]
    print(df1)
    sentiment_percentages = result_df_melted.pivot(index="Date", columns="Sentiment", values="Count")
    df1 = pd.merge(df1, sentiment_percentages, how="left", left_on="Date", right_index=True)
    print(df1.columns)
    # Print column names and data types
    print(df1.dtypes)
    df1['positive_larger'] = df1['Positive'] > df1['Negative']
    # Print the first few rows of the DataFrame
    print(df1.head())
    # Try scatter plot of `Adj Close`
    fig = px.line(
        df1,
        x="Date",
        y="Price",
        color='Instrument',
        title="Stock Prices Over Time",
        hover_data=["Negative", "Positive"],
        labels={
            "Date": "Date",
            "Price": "Price",
            "Instrument": "Instrument",
            "Negative": "Negative %",
            "Positive": "Positive %",
        },
        markers=True
    )
    
    fig.update_xaxes(
        dtick="D1",  
        tickformat="%Y-%m-%d",  
    )
    return fig.to_html()


def News_Cumulative_Diff_Graph(data):
    fig = px.line(
        data,
        x="Date",
        y="Cumulative_Difference",
        labels={"value": "Percentage", "variable": "Sentiment"},
        title="Cumulative Positive - Negative Sentiment Over Time",
    )
    fig.write_html("static/cumulative_news_data.html")


@app.route("/")
def index():
    """simple index page"""
    news = fetch_news()
    return render_template("index.html", news=news)


@app.route("/news/<category>")
def get_news(category):
    # Fetch news based on the category
    all_news = fetch_news()
    return jsonify({"articles": all_news})


@app.route("/update_graphs")
def update_graphs():
    print(request)
    # start_date = request.args.get("start")
    # end_date = request.args.get("end")

    # Use start_date and end_date in your graph functions (e.g., fetch data within this date range)
    # Example: fetch_data_within_date_range(start_date, end_date)
    # Perform operations to update graphs based on the provided date range

    # For example, assuming you have functions to update graphs based on date range
    # weekly_stocks_graph_spy(start_date, end_date)
    # Return a response (you can provide some data if needed)
    return jsonify({"message": "Graphs updated successfully"})


@app.route("/generate_graph", methods=["GET"])
def generate_graph():
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    ticker = request.args.get("ticker")

    print(start_date, end_date, ticker)
    # Call your Python function to generate the graph data
    graph_data = weekly_stocks_graph_spy(start_date, end_date, ticker)
    # lol
    return jsonify(graph_data)


@app.route("/about", methods=["GET"])
def about():
    """returns study html template"""
    return render_template("about.html")


if __name__ == "__main__":
    # weekly_stocks_graph_spy("2021-04-01", "2023-04-30", ticker="XLE")
    app.run(debug=True, port=9000)
    # get_stocks_for_week()
