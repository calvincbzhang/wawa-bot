from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
account_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, account_token)

message = client.messages.create(
                            body='Hello There',
                            media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
                            from_='whatsapp:+1415523886',
                            to='whatsapp:+447708438644'
                        )

print(message.sid)
