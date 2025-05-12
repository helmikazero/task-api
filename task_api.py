from flask import Flask, request, jsonify
import requests
import datetime
import json
import os

# ---- Google Task API Configuration ----
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN")
TASK_LIST_ID = os.environ.get("GOOGLE_TASK_LIST_ID")

TOKEN_URL = "https://oauth2.googleapis.com/token"

def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def create_task(title, notes, due_date):
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    task_data = {
        "title": title,
        "notes": notes,
        "due": due_date + "T00:00:00.000Z"
    }

    response = requests.post(
        f"https://tasks.googleapis.com/tasks/v1/lists/{TASK_LIST_ID}/tasks",
        headers=headers,
        json=task_data
    )
    response.raise_for_status()
    return response.json()

# ---- Flask API ----

app = Flask(__name__)

@app.route("/create-task", methods=["POST"])
def create():
    try:
        data = request.json
        title = data["title"]
        notes = data.get("notes", "")
        due_date = data["due_date"]
        task = create_task(title, notes, due_date)
        return jsonify({"status": "success", "task_id": task["id"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

