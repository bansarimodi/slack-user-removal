import os
from flask import Flask, request
from detect_removal import scan_event
from send_dm_csm import notify_csm

app = Flask(__name__)


@app.route("/slack/events", methods=["POST"])
def slack_events():

    event = request.json

    is_removal, username, channel_id = scan_event(event)

    if is_removal:
        notify_csm(username, channel_id)

    return {"status": "ok"}


@app.route("/")
def home():
    return "Slack webhook bot running."


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 3000))

    app.run(host="0.0.0.0", port=port)