import requests
from config import CLOSE_API_KEY

SEARCH_URL = "https://api.close.com/api/v1/data/search/"
CONTACT_URL = "https://api.close.com/api/v1/contact/"


def normalize_name(name):

    return name.lower().replace(".", "").strip()


def get_contact_details(contact_id):

    try:

        response = requests.get(
            f"{CONTACT_URL}{contact_id}/",
            auth=(CLOSE_API_KEY, "")
        )

        if response.status_code != 200:
            return None

        return response.json()

    except Exception as e:

        print("Contact fetch failed:", e)

        return None


def search_contact(slack_name):

    print("Searching Close CRM:", slack_name)

    slack_name = normalize_name(slack_name)

    search_payload = {
        "query": {
            "type": "and",
            "queries": [
                {
                    "type": "object_type",
                    "object_type": "contact"
                },
                {
                    "type": "text",
                    "field": "name",
                    "value": slack_name,
                    "mode": "full_words"
                }
            ]
        }
    }

    cursor = None
    backup = None

    while True:

        try:

            if cursor:
                search_payload["cursor"] = cursor

            response = requests.post(
                SEARCH_URL,
                json=search_payload,
                auth=(CLOSE_API_KEY, "")
            )

            if response.status_code != 200:
                return None

            result = response.json()

        except Exception as e:

            print("Search failed:", e)

            return None

        contacts = result.get("data", [])

        for contact in contacts:

            contact_id = contact.get("id")

            if not contact_id:
                continue

            contact_data = get_contact_details(contact_id)

            if not contact_data:
                continue

            emails = contact_data.get("emails")

            if not emails:
                continue

            email = emails[0]["email"]

            lead_id = contact_data.get("lead_id")

            contact_name = normalize_name(
                contact_data.get("name", "")
            )

            if slack_name == contact_name:

                return {
                    "email": email,
                    "lead_id": lead_id
                }

            if not backup:

                backup = {
                    "email": email,
                    "lead_id": lead_id
                }

        cursor = result.get("cursor")

        if not cursor:
            break

    return backup