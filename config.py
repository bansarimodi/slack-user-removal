import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CSM_SLACK_USER_ID = os.getenv("CSM_SLACK_USER_ID")

HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

SLACK_REMOVAL_MESSAGE = "has removed themselves from this channel"