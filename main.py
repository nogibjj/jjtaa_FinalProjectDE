from dotenv import load_dotenv
import os
from flask import Flask, render_template
from databricks import sql

load_dotenv()

app = Flask(__name__)

# Azure Databricks API token
DATABRICKS = os.getenv("DATABRICKS")
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")


# Function to get news from the warehouse
def get_random_news():
    """gets random news"""
    server_h = DATABRICKS_HOST
    access_token = DATABRICKS
    http_path = DATABRICKS_PATH
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute("SELECT * FROM default.news ORDER BY RAND() LIMIT 5;")
        result = c.fetchall()
        return result


@app.route("/")
def index():
    """simple index page"""
    news = get_random_news()
    return render_template("index.html", news=news)


if __name__ == "__main__":
    app.run(debug=True)
