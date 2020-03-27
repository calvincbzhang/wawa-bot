from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

import io
from PIL import Image
import os
import hashlib
import csv
import time
from bs4 import BeautifulSoup as soup

app = Flask(__name__)

def get_image():
  url = "https://old.reddit.com/r/Coronavirus_Meme/"
  # Headers to mimic a browser visit
  headers = {'User-Agent': 'Mozilla/5.0'}

  # Returns a requests.models.Response object
  page = requests.get(url, headers=headers)

  soup_page = soup(page.text, 'html.parser')

  attrs = {'class': 'thing', 'data-domain': 'i.redd.it'}

  counter = 1

  # TODO fix get_image function so that is returns the most relevant image with text as well
  while (counter <= 30):
    posts = soup_page.find_all('div', attrs=attrs)
    for post in posts:
      image = post.find("a", class_="thumbnail")
      image_page_link = 'http://old.reddit.com' + image.attrs['href'] + '?'
      image_page = requests.get(image_page_link, headers=headers)
      image_soup_page = soup(image_page.text, 'html.parser')
      
      file = image_soup_page.find("img", class_="preview")
      file_link = file.attrs['src']
      
      return file_link

      counter += 1

    next_button = soup_page.find("span", class_="next-button")
    next_page_link = next_button.find("a").attrs['href']
    time.sleep(2)
    page = requests.get(next_page_link, headers=headers)
    soup_page = soup(page.text, 'html.parser')

GOOD_BOY_URL = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"

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
    msg = resp.message("You walking or you working hun.")
  elif (msg == "Meme"):
    msg = resp.message("Here is your meme of the day")
    msg.media(get_image())
  else:
    msg = resp.message("Good Night Calvin")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)