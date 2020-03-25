from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
account_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, account_token)

