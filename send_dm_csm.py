import requests
from config import HEADERS, CSM_SLACK_USER_ID


def get_channel_name(channel_id):

    response = requests.get(
        "https://slack.com/api/conversations.info",
        headers=HEADERS,
        params={"channel": channel_id}
    )

    data = response.json()

    if data.get("ok"):
        return data.get("channel", {}).get("name", channel_id)
    else:
        return channel_id


def notify_csm(username, channel_id):

    channel_name = get_channel_name(channel_id)

    message = (
        f":warning:Slack Connect User Removed\n"
        f"User: {username}\n"
        f"Channel: #{channel_name}\n"
        f"Trial likely expired. Please re-invite via Slack Connect."
    )

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=HEADERS,
        json={
            "channel": CSM_SLACK_USER_ID,
            "text": message
        }
    )

    data = response.json()

    if data.get("ok"):
        print(f"CSM notified: {username} removed from #{channel_name}")
    else:
        print(f"Failed to notify CSM: {data.get('error')}")