from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
account_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, account_token)

message = client.messages.create(
                            body='Hello There',
                            from_='whatsapp:+1415523886'
                            to='whatsapp:+447708438644'
                        )

print(message.sid)
