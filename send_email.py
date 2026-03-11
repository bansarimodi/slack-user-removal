import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_EMAIL, SMTP_PASSWORD


def send_invite_email(user_email, csm_email):

    try:

        subject = "Slack Channel Reinvite"

        body = """
Hi,

You have been re-added to your Slack private channel.

Please login to Slack to access it.

Your CSM is copied if you need help.

Thanks
Data Engineer Academy
"""

        msg = MIMEMultipart()

        msg["From"] = SMTP_EMAIL
        msg["To"] = user_email
        msg["Cc"] = csm_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        recipients = [user_email, csm_email]

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.ehlo()

        server.starttls()

        server.ehlo()

        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        server.sendmail(
            SMTP_EMAIL,
            recipients,
            msg.as_string()
        )

        print("Email sent successfully")

        server.quit()

    except Exception as e:

        print("Email failed:", e)