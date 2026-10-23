import os
import logging

from flask import Flask, request, jsonify

app = Flask(__name__)

LOG_DIR = "/app/logs"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(LOG_DIR, "notification.log")
        )
    ]
)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    logging.info("Notification received for message: %s", message)

    return jsonify({
        "status": "notification recorded",
        "message": message
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
