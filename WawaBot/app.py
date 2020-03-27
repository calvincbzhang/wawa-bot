from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

@app.route("/")
def home_reply():
  return "Hello World"

@app.route("/sms", methods=['POST'])
def whatsapp_reply():
  """
    Respond to basic message on whatsapp
  """
  msg = request.form.get('Body')

  #Start out response
  resp = MessagingResponse()

  if (msg == "Hello"):
    resp.message("You walking or you working hun.")
  else:
    resp.message("Good Night Calvin")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)