from detect_removal import scan_event
from search_email_close import search_contact
from get_csm_lead import get_csm_from_lead
from slack_invite import invite_user
from send_email import send_invite_email


def process_event(event):


    is_removal, user_info, channel_id = scan_event(event)

    if not is_removal:

        print("Not removal event")

        return

    user_value = user_info["value"]

    print("User:", user_value)

    print("Channel:", channel_id)

    contact = search_contact(user_value)

    if not contact:

        print("Contact not found")

        return

    user_email = contact["email"]

    lead_id = contact["lead_id"]

    print("User email:", user_email)

    csm_email = get_csm_from_lead(lead_id)

    if not csm_email:

        print("CSM not found")

        return

    print("CSM:", csm_email)

    invite_result = invite_user(
        user_email,
        channel_id,
        user_value
    )

    if invite_result.get("ok"):

        print("User invited to channel")

    else:

        error = invite_result.get("error")

        if error == "already_in_channel":

            print("User already in channel")

        elif error == "users_not_found":

            print("User not in workspace")

        else:

            print("Slack invite failed")

    send_invite_email(
        user_email,
        csm_email
    )


if __name__ == "__main__":

    test_event = {

        "type": "message",

        "text":
        "hlopez has removed themselves from this channel",
        "channel": "C0A16PK3YSW"

    }

    process_event(test_event)