"""
Test goes here

"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Azure Databricks API token
DATABRICKS = os.getenv("DATABRICKS")
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_PATH = os.getenv("DATABRICKS_PATH")

FILESTORE_PATH = ""
url = f"https://{DATABRICKS_HOST}/api/2.0"

# test html files
def test_html_files(directory="templates/"):
    """checks html files exists"""
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

    for html_file in html_files:
        file_path = os.path.join(directory, html_file)
        assert os.path.exists(file_path) and os.path.isfile(file_path)


def check_filestore_path(path, headers):
    try:
        response = requests.get(url + f"/dbfs/get-status?path={path}", headers=headers)
        response.raise_for_status()
        return response.json()["path"] is not None
    except Exception as e:
        print(f"Error checking file path: {e}")
        return False


# Test if the specified FILESTORE_PATH exists
def test_databricks():
    headers = {"Authorization": f"Bearer {DATABRICKS}"}
    assert check_filestore_path(FILESTORE_PATH, headers) is False


if __name__ == "__main__":
    test_html_files()
    test_databricks()
