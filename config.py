import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CLOSE_API_KEY = os.getenv("CLOSE_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SLACK_REMOVAL_MESSAGE = "has removed themselves from this channel"

HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

if not all([SLACK_BOT_TOKEN, CLOSE_API_KEY, SMTP_EMAIL, SMTP_PASSWORD]):
    raise ValueError("Missing environment variables")