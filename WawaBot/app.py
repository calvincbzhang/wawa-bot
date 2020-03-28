from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup as soup
import requests
import time
from random import randint
import json

app = Flask(__name__)

JOKES = ['A blind man walks into a bar. And a table. And a chair.', 'Why do Dasher and Dancer love coffee? Because they are Santas star bucks.', 'What do you get when you cross a christmas tree with an apple?  A pineapple.', 'What do you call a guy with a rubber toe? Roberto.', 'Why did the old man fall in the well? Because he couldn\'t see that well.', 'I know a lot of jokes about unemployed people but none of them work.', 'What\'s orange and sounds like a parrot? A carrot.',
        'Parallel lines have so much in common. It’s a shame they will never meet.', 'What did one hat say to the other? You stay here. I will go on ahead.', 'Oh Ryans belt is a big waist of space. Alright that was a terrible joke. I give it three stars. It was a stellar performance though.', 'Did you hear about the crook who stole the calendar? He got twelve months.', 'I have the worlds worst thesaurus. Not only is it terrible, it is  terrible.',
        'I woke up this morning and forgot the direction from which the sun rises. Then it dawned on me.', 'The problem with kleptomaniacs is that they always take things, literally.', 'Did you hear about the restaurant on the moon? Great food, no atmosphere.', 'Want to hear a joke about paper? Nevermind it\'s tearable.', 'Why did the coffee file a police report? It got mugged.', 'What do you call cheese that isn\'t yours? Nacho Cheese.',
        'Why couldn\'t the bicycle stand up by itself? It was two tired.', 'This graveyard looks overcrowded. People must be dying to get in there.', 'What\'s brown and sticky? A stick.', 'A furniture store keeps calling me. All I wanted was one night stand.', 'I thought about going on an all almond diet. But that iss just nuts.', 'Did you hear about the kidnapping at school? It is fine, he woke up.', 'This graveyard looks overcrowded. People must be dying to get in there.',
        'I wouldn\'t buy anything with velcro. It is a total rip off.', 'How does a penguin build its house? Igloos it together.', 'Why did the scarecrow win an award? Because he was outstanding in his field. But hay, it must run in his jeans.']

def wawa_tell_who_reccomendations():
  reccomendations = """Wash your hands frequently.\n Maintain social distancing.\n Avoid touching eyes, nose and mouth. 
  \n Practice respiratory hygiene. \n If you have fever, cough and difficulty breathing, seek medical care early. 
  \n Stay informed and follow advice given by your healthcare provider."""

  return reccomendations

def wawa_get_emergency(country):
  with open("countries.txt") as json_file:
    data = json.load(json_file)
  
  US_list = ["usa", "merica", "us", "united states of america", "america"]
  UK_list = ["scotland", "northern ireland", "wales", "england", "britain", "great britain", "uk"]
  UAE_list = ["uae"]
  
  if (country.lower() in US_list):
    country = "United States"
  elif (country.lower() in UK_list):
    country = "United Kingdom"
  elif (country.lower() in UAE_list):
    country = "United Arab Emirates"
  
  if "ambulance" not in data[country] and "police" not in data[country]:
    return data[country]["single"]  
  return data[country]["ambulance"]

def wawa_tell_welcome():
  #TO DO starting instriuctions
  message = """Wawa-wee-wa buddy. Welcome to a fun and instructive space, to get the straight facts and fun you need in this strange time.
  You can ask me a lot of things. \n Ask: latest reccomendations - to see the latest reccomendations by WHO and obtain the URL for myth busters
  and all the info to keep you safe. \n Ask me to tell you a joke. \n Ask me for a: meme. \n Ask me for an: update [in your country] i.e. update UK.
  Ask me if you have an emergency for your national emergency number: emergency [country]. \n If you have forgotten the way to ask me for info ask for: instructions:."""

  return message

def wawa_tell_instructions():
  message = """You can ask me a lot of things. \n Ask: latest reccomendations - to see the latest reccomendations by WHO and obtain the URL for myth busters
  and all the info to keep you safe. \n Ask me to tell you a joke. \n Ask me for a: meme. \n Ask me for an: update [in your country] i.e. update UK.
  \n Ask me if you have an emergency for your national emergency number: emergency [country]. \n If you have forgotten the way to ask me for info ask for: instructions:."""

  return message

def wawa_tell_joke():
  num_jokes = len(JOKES) - 1
  chosen_joke_index = randint(0, num_jokes)
  joke = JOKES[chosen_joke_index]

  for i in range(len(joke)):
    if joke[i] == '.' or joke[i] == '?':
      return joke[0:i+1] + "\n.\n.\n.\n.\n.\n" + joke[i+1:]

def wawa_update_message(confirmed, deaths, recov, total_conf, country):
  wawa_info_builder = " Today in {}, we recorded {} new confirmed cases, we have the pleasure of announcing that {} recovered, welcome back to them! We mourn the passing of {} people. There are now {} cases.".format(country, confirmed, recov, deaths, total_conf)
  
  return wawa_info_builder

def covid_api(country):
  """
    Simple test
  """
  response = requests.get("https://api.covid19api.com/summary")

  #Ensure connection with API
  if (response.status_code != 200):
    return "Failed to connect with API"
  else:
    response_json = response.json()
    count = 0
  
  US_list = ["usa", "merica", "united states", "united states of america", "america"]
  UK_list = ["scotland", "northern ireland", "wales", "england", "britain", "great britain", "uk"]
  UAE_list = ["uae"]
  
  if (country.lower() in US_list):
    country = "US"
  elif (country.lower() in UK_list):
    country = "United Kingdom"
  elif (country.lower() in UAE_list):
    country = "United Arab Emirates"

  country_tolower = country.lower()

  while(True):
    if response_json['Countries'][count]['Country'].lower() == country_tolower:
      new_confirmed = response_json['Countries'][count]['NewConfirmed']
      new_deaths =  response_json['Countries'][count]['TotalDeaths']
      new_recovered = response_json['Countries'][count]['NewRecovered']
      total_confirmed = response_json['Countries'][count]['TotalConfirmed']
      return wawa_update_message(new_confirmed, new_deaths, new_recovered, total_confirmed, country)
    if response_json['Countries'][count]['Country'] == "Zimbabwe":
      break
    count += 1
  return "Sorry you must have written a wrong country name."

def wawa_get_meme():
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

  greeting_list = ["hey", "good morning", "good evening", "good morrow", "hello", "hi", "what's up", "yo", "sup"]
  joke_list = ["bored", "joke", "laugh", "boring"]

  if (msg.lower() in greeting_list):
    msg = resp.message(wawa_tell_welcome())
  elif ( "meme" in msg.lower()):
    image, message = wawa_get_meme()
    msg = resp.message(message).media(image)
  elif (any(joke in msg.lower() for joke in joke_list)):
    if randint(0,1) == 0:
      image, message = wawa_get_meme()
      msg = resp.message(message).media(image)
    else:
      msg = resp.message(wawa_tell_joke())
  elif ("update" in msg.lower()):
    country = msg[7:]
    msg = resp.message(covid_api(country))
  elif ("instructions" in msg.lower()):
    msg = resp.message(wawa_tell_instructions())
  elif ("emergency" in msg.lower()):
    country = msg[10:]
    print(country)
    msg = resp.message(wawa_get_emergency(country))
  elif ("who" in msg.lower() or "reccomendations" in msg.lower() or "world health organisation" in msg.lower()):
    msg = resp.message(wawa_tell_who_reccomendations())
  else:
    msg = resp.message("Sorry I did not catch that, ask me for: instructions or emergency:.")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)