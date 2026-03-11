import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL=os.getenv("SMTP_EMAIL")
PASSWORD=os.getenv("SMTP_PASSWORD")


try:

    server=smtplib.SMTP_SSL("smtp.gmail.com",465)

    server.login(EMAIL,PASSWORD)

    print("LOGIN SUCCESS ✅")

    server.quit()

except Exception as e:

    print("LOGIN FAILED ❌")
    print(e)