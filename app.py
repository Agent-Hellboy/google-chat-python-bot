"""Example bot which execute python expression and returns a local execution environment which is enough to teach the concept"""

import io
import sys
import traceback

from flask import Flask, json, request

app = Flask(__name__)


def _exec(code: str) -> str:
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
    stdout, stderr, exc = "", "", ""
    try:
        exec(code.strip())
    except Exception:
        exc = traceback.format_exc()
    stdout, stderr = sys.stdout.getvalue(), sys.stderr.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr
    return exc.strip() or stderr.strip() or stdout.strip() or "Success"


@app.route("/", methods=["POST"])
def on_event():
    """Handles an event from Google Chat."""
    event = request.get_json()
    if event["type"] == "ADDED_TO_SPACE":
        text = f"Thanks for adding me to {event['space']['displayName']}!"

    elif event["type"] == "REMOVED_FROM_SPACE":
        text = f"Bye Bye,nice tille stay at {event['space']['displayName']}!"

    elif event["type"] == "MESSAGE":
        if event["message"]["text"].startswith("@python exec"):
            message = event["message"]["text"].split("@python exec")
            text = f"```{_exec(message[1][1:])}```"

    return json.jsonify({"text": text})
