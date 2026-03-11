import requests
from config import CLOSE_API_KEY

LEAD_URL = "https://api.close.com/api/v1/lead/"
USER_URL = "https://api.close.com/api/v1/user/"


def get_csm_from_lead(lead_id):

    try:

        lead_response = requests.get(
            f"{LEAD_URL}{lead_id}/",
            auth=(CLOSE_API_KEY, "")
        )

        if lead_response.status_code != 200:
            return None

        lead_data = lead_response.json()

        csm_user_id = lead_data.get("custom", {}).get("CSM")

        if not csm_user_id:
            return None

        user_response = requests.get(
            f"{USER_URL}{csm_user_id}/",
            auth=(CLOSE_API_KEY, "")
        )

        if user_response.status_code != 200:
            return None

        return user_response.json().get("email")

    except Exception as e:

        print("CSM lookup failed:", e)

        return None