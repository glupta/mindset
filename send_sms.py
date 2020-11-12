# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC60290cea8f4b0236d39320e2bfe3e4bf'
auth_token = '4843ea93ed857bceec7e8c42907c98b1'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+13158205380',
                     to='+16314561585'
                 )

print(message.sid)