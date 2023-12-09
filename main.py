from dotenv import load_dotenv
import os
from flask import Flask, render_template, jsonify
from databricks import sql

# import openai
from datetime import datetime, timedelta
import pytz
import pandas as pd
import plotly.express as px


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
        days_back = 7
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=days_back)

        # Filter data for the closest week
        closest_week_data = [
            entry
            for entry in result
            if week_start <= entry["Date"].astimezone(pytz.UTC) <= week_end
        ]
        return closest_week_data


def weekly_stocks_graph():
    """Saves the graph as an HTML file"""
    # converting the data to a pandas dataframe
    data = get_stocks_for_week()
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

    # print(df['Price_type'].unique())
    
    # Convert Date column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    
    df1 = df[df['Price_type']=="Adj Close"]

    # Plotting with Plotly
    # fig = px.line(
    #     df1,
    #     x="Date",
    #     y="Price",
    #     color="Instrument",
    #     line_group="Price_type",
    #     title="Stock Prices Over Time",
    #     labels={
    #         "Date": "Date",
    #         "Price": "Price",
    #         "Instrument": "Instrument",
    #         "Price_type": "Price Type",
    #     },
    # )
    
    # # Try scatter plot of `Adj Close`
    fig = px.scatter(
    df1,
    x="Date",
    y="Price",
    color="Instrument",
    symbol="Price_type",  # This will use different symbols for each 'Price_type'
    title="Stock Prices Over Time",
    labels={
        "Date": "Date",
        "Price": "Price",
        "Instrument": "Instrument",
        # "Price_type": "Price Type",
    },
    )
    fig.write_html("static/stocks_graph.html")


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


@app.route("/about", methods=["GET"])
def about():
    """returns study html template"""
    return render_template("about.html")


if __name__ == "__main__":
    weekly_stocks_graph()
    app.run(debug=True, port=9000)
    # get_stocks_for_week()
