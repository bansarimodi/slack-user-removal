import requests
from config import HEADERS


def get_user_id_by_email(email):

    try:

        response = requests.get(
            "https://slack.com/api/users.lookupByEmail",
            headers=HEADERS,
            params={"email": email}
        )

        data = response.json()

        if data.get("ok"):

            print("Slack user found by email")

            return data["user"]["id"]

    except Exception as e:

        print("Slack email lookup failed:", e)

    return None


def get_user_id_by_name(name):

    try:

        response = requests.get(
            "https://slack.com/api/users.list",
            headers=HEADERS
        )

        data = response.json()

        if not data.get("ok"):
            return None

        name = name.lower()

        for user in data["members"]:

            real = (user.get("real_name") or "").lower()

            display = (
                user.get("profile", {})
                .get("display_name", "")
                .lower()
            )

            username = (user.get("name") or "").lower()

            if name in real or name in display or name in username:

                print("Slack user found by name")

                return user["id"]

    except Exception as e:

        print("Slack name lookup failed:", e)

    return None


def invite_user(email, channel_id, name):

    user_id = get_user_id_by_email(email)

    if not user_id:

        print("Trying name lookup")

        user_id = get_user_id_by_name(name)

    if not user_id:

        return {
            "ok": False,
            "error": "users_not_found"
        }

    try:

        response = requests.post(
            "https://slack.com/api/conversations.invite",
            headers=HEADERS,
            json={
                "channel": channel_id,
                "users": user_id
            }
        )

        data = response.json()

        print("Slack response:", data)

        return data

    except Exception as e:

        print("Slack invite failed:", e)

        return {"ok": False}