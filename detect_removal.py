from config import SLACK_REMOVAL_MESSAGE


def extract_user(text):

    if not text:
        return None

    user = text.split(SLACK_REMOVAL_MESSAGE)[0].strip()

    if "'s workspace" in user:
        user = user.split("'s")[0]

    user = user.strip().lower()
    user = user.replace(".", "")
    user = user.replace("_", " ")

    if not user:
        return None

    if "@" in user:
        return {
            "type": "email",
            "value": user
        }

    return {
        "type": "name",
        "value": user
    }


def scan_event(event):

    print("\n===== SCANNING EVENT =====")

    if not event:
        return False, None, None

    event_type = event.get("type")

    if event_type == "member_left_channel":

        print("Member left channel detected")

        return True, {
            "type": "user_id",
            "value": event.get("user")
        }, event.get("channel")

    text = (event.get("text") or "").lower()

    if event_type == "message" and SLACK_REMOVAL_MESSAGE in text:

        print("Slackbot removal detected")

        user = extract_user(text)

        if not user:
            return False, None, None

        return True, user, event.get("channel")

    return False, None, None