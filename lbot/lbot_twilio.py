# twilio.py


import os
from dotenv import load_dotenv

from twilio.rest import Client

import lbot_slack as slack
import lbot_data as data


load_dotenv()
try:
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
except:
    print("Error: No Twilio Account SID found in environment variables!")
    raise EnvironmentError

try:
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
except:
    print("Error: No Twilio Auth Token found in environment variables!")
    raise EnvironmentError


# get number of recipient from address book
def get_number(recipient):
    if recipient.title() in data.address_book:
        number = data.address_book[recipient.title()]
        return number
    else:
        return None


# send SMS via twilio API
def send_sms(msg, number, author):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(body=msg, from_="+12055573240", to=number)

    slack.post("SMS message sent via twilio with SID: " + message.sid)

    return
