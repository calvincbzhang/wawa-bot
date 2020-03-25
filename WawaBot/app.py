from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def home_reply():
  return "Hello World"

@app.route("/sms", methods=['POST'])
def whatsapp_reply():
  """
    Respond to basic message on whatsapp
  """
  msg = request.form.get('body')

  #Start out response
  resp = MessagingResponse()

  #Add a message
  resp.message("")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)