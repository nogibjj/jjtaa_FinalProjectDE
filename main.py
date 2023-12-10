from dotenv import load_dotenv
import os
from flask import Flask, render_template, jsonify
from databricks import sql

# import openai
from datetime import datetime, timedelta
import pytz
import pandas as pd
import plotly.express as px
import numpy as np
from requests import request

# from NewsViz import *


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
        c.execute("SELECT * FROM default.news LIMIT 5;")
        result = c.fetchall()
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
    """Saves the graph as an HTML file"""
    # converting the data to a pandas dataframe
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
    df = pd.DataFrame(data_list)

    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    df1 = df[df["Price_type"] == "Adj Close"]
    df1 = df1[df1["Instrument"] == ticker]
    if start_date < "2023-11-05":
        start_date = "2023-11-05"
    if end_date < "2023-11-05":
        end_date = "2023-11-11"
    df1 = df1[(df1["Date"] >= start_date) & (df1["Date"] <= end_date)]

    # # Try scatter plot of `Adj Close`
    fig = px.line(
        df1,
        x="Date",
        y="Price",
        color="Instrument",
        title="Stock Prices Over Time",
        labels={
            "Date": "Date",
            "Price": "Price",
            "Instrument": "Instrument",
            # "Price_type": "Price Type",
        },
    )
    fig.update_xaxes(
        dtick="D1",  # Specifies that ticks should be shown every 1 day
        tickformat="%Y-%m-%d",  # Customize date format if needed
    )
    fig.update_layout(xaxis=dict(range=[start_date, end_date]))
    # fig.write_html("static/stocks_graph.html")
    fig.show()


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
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    # Use start_date and end_date in your graph functions (e.g., fetch data within this date range)
    # Example: fetch_data_within_date_range(start_date, end_date)
    # Perform operations to update graphs based on the provided date range

    # For example, assuming you have functions to update graphs based on date range
    weekly_stocks_graph_spy(start_date, end_date)
    # Return a response (you can provide some data if needed)
    return jsonify({"message": "Graphs updated successfully"})


@app.route("/about", methods=["GET"])
def about():
    """returns study html template"""
    return render_template("about.html")


if __name__ == "__main__":
    # weekly_stocks_graph_spy("2021-04-01", "2023-04-30", ticker="XLE")
    app.run(debug=True, port=9000)
    # get_stocks_for_week()
