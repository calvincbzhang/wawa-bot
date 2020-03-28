from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import time
from bs4 import BeautifulSoup as soup
from random import randint

app = Flask(__name__)

def get_image():
  url = "https://old.reddit.com/r/Coronavirus_Meme/"
  # Headers to mimic a browser visit
  headers = {'User-Agent': 'Mozilla/5.0'}

  # Returns a requests.models.Response object
  page = requests.get(url, headers=headers)

  soup_page = soup(page.text, 'html.parser')

  attrs = {'class': 'thing', 'data-domain': 'i.redd.it'}

  counter = 0
  page_number = 0

  images = []
  messages = []

  while (True):
    posts = soup_page.find_all('div', attrs=attrs)
    for post in posts:
      # gets the link for the image
      thumbnail = post.find("a", class_="thumbnail")
      thumbnail_page_link = 'http://old.reddit.com' + thumbnail.attrs['href'] + '?'
      image_page = requests.get(thumbnail_page_link, headers=headers)
      image_soup_page = soup(image_page.text, 'html.parser')
      file = image_soup_page.find("img", class_="preview")
      file_link = file.attrs['src']
      images.append(file_link)

      # gets the meme message
      entry = post.find("div", class_="entry")
      messages.append(entry.div.p.a.text)

      counter += 1

      if (counter == 10):
        index = randint(0, len(images) - 1)

        return images[index], messages[index]

    next_button = soup_page.find("span", class_="next-button")
    next_page_link = next_button.find("a").attrs['href']
    page = requests.get(next_page_link, headers=headers)
    soup_page = soup(page.text, 'html.parser')

  index = randint(0, len(images) - 1)

  return images[index], messages[index]


@app.route("/")
def home_reply():
  return "Hello World"

@app.route("/sms", methods=['POST'])
def whatsapp_reply():
  """
    Respond to basic message on whatsapp
  """
  msg = request.form.get('Body')

  # Start out response
  resp = MessagingResponse()

  if (msg == "Hello"):
    msg = resp.message("You walking or you working hun.")
  elif (msg == "Meme"):
    image, message = get_image()
    msg = resp.message(message)
    msg.media(image)
  else:
    msg = resp.message("Good Night Calvin")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)