import os
import logging
import requests

from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000")

logging.basicConfig(level=logging.INFO)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lab 7 - Microservices</title>
</head>
<body>
    <h1>Docker Microservices Lab</h1>

    <h2>Create a Message</h2>

    <form action="/send" method="POST">
        <input
            type="text"
            name="message"
            placeholder="Enter your message"
            required
        >
        <button type="submit">Send</button>
    </form>

    <h2>Messages</h2>

    {% if error %}
        <p style="color:red">{{ error }}</p>
    {% endif %}

    <ul>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
    </ul>

    <a href="/">Refresh Messages</a>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    messages = []
    error = None

    try:
        response = requests.get(
            f"{BACKEND_URL}/messages",
            timeout=5
        )
        response.raise_for_status()
        messages = response.json().get("messages", [])

    except requests.RequestException as exc:
        logging.error("Failed to connect to backend: %s", exc)
        error = "Backend service is unavailable."

    return render_template_string(
        HTML_PAGE,
        messages=messages,
        error=error
    )


@app.route("/send", methods=["POST"])
def send_message():
    message = request.form.get("message", "").strip()

    if message:
        try:
            response = requests.post(
                f"{BACKEND_URL}/messages",
                json={"message": message},
                timeout=10
            )
            response.raise_for_status()

        except requests.RequestException as exc:
            logging.error("Failed to submit message: %s", exc)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
