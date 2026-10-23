import os
import json
import logging
import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_DIR = "/app/data"
DATA_FILE = os.path.join(DATA_DIR, "messages.json")
LOG_DIR = "/app/logs"

NOTIFICATION_URL = os.getenv(
    "NOTIFICATION_URL",
    "http://notification:5001/notify"
)

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(LOG_DIR, "backend.log")
        )
    ]
)


def load_messages():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        logging.exception("Failed to read stored messages")
        return []


def save_messages(messages):
    temporary_file = DATA_FILE + ".tmp"

    with open(temporary_file, "w") as file:
        json.dump(messages, file, indent=2)

    os.replace(temporary_file, DATA_FILE)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/messages", methods=["GET"])
def get_messages():
    logging.info("Received request to retrieve messages")

    return jsonify({"messages": load_messages()})


@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    messages = load_messages()
    messages.append(message)
    save_messages(messages)

    logging.info("Message created successfully: %s", message)

    try:
        response = requests.post(
            NOTIFICATION_URL,
            json={"message": message},
            timeout=3
        )
        response.raise_for_status()

        logging.info("Notification sent successfully")

    except requests.RequestException:
        logging.exception("Failed to send notification")

    return jsonify({
        "status": "success",
        "message": message
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
