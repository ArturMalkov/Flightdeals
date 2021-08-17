from twilio.rest import Client
import requests
import smtplib
import os

#please register with Twilio to obtain your own account_sid, auth_token and us_phone_number
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
US_PHONE_NUMBER = os.environ.get("US_PHONE_NUMBER")

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

YOUR_PHONE_NUMBER = os.environ.get("YOUR_PHONE_NUMBER") #notifications will be sent to this number


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def sending_message(self, message):
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body=message,
            from_=US_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )

        print(message.sid)

    def send_emails(self, addressee, text):
        with smtplib.SMTP("smtp.mail.Yahoo.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=addressee,
                msg=text,
            )
