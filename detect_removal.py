from config import SLACK_REMOVAL_MESSAGE


def get_username(text):

    if SLACK_REMOVAL_MESSAGE in text:
        username = text.split(SLACK_REMOVAL_MESSAGE)[0]
        return username.strip()
    else:
        return "Unknown User"


def scan_event(event):

    event_type = event.get("type")
    subtype = event.get("subtype", "")
    text = event.get("text", "").lower()
    channel_id = event.get("channel", "")

    if event_type == "member_left_channel":
        print("Removal detected via member_left_channel")
        return True, "User", channel_id

    elif event_type == "message" and subtype == "channel_leave":
        print("Removal detected via channel_leave")
        username = get_username(text)
        return True, username, channel_id

    elif event_type == "message" and SLACK_REMOVAL_MESSAGE in text:
        print("Removal detected via Slackbot message")
        username = get_username(text)
        return True, username, channel_id

    else:
        return False, None, None