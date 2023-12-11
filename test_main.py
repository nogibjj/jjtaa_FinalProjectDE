"""
Test goes here

"""
import os

# Azure Databricks API token
# DATABRICKS = os.getenv("DATABRICKS")
# DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
# DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")

# test html files
def test_html_files(directory="templates/"):
    """checks html files exists"""
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

    for html_file in html_files:
        file_path = os.path.join(directory, html_file)
        assert os.path.exists(file_path) and os.path.isfile(file_path)


if __name__ == "__main__":
    test_html_files()
    # test_databricks()
