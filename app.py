from flask import Flask, request, send_from_directory, render_template
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup as soup
import urllib
import requests
import time
from random import randint
import json
import os

app = Flask(__name__)

JOKES = ['A blind man walks into a bar. And a table. And a chair.', 'Why do Dasher and Dancer love coffee? Because they are Santas star bucks.', 'What do you get when you cross a christmas tree with an apple?  A pineapple.', 'What do you call a guy with a rubber toe? Roberto.', 'Why did the old man fall in the well? Because he couldn\'t see that well.', 'I know a lot of jokes about unemployed people but none of them work.', 'What\'s orange and sounds like a parrot? A carrot.',
        'Parallel lines have so much in common. It’s a shame they will never meet.', 'What did one hat say to the other? You stay here. I will go on ahead.', 'Oh Ryans belt is a big waist of space. Alright that was a terrible joke. I give it three stars. It was a stellar performance though.', 'Did you hear about the crook who stole the calendar? He got twelve months.', 'I have the worlds worst thesaurus. Not only is it terrible, it is  terrible.',
        'I woke up this morning and forgot the direction from which the sun rises. Then it dawned on me.', 'The problem with kleptomaniacs is that they always take things, literally.', 'Did you hear about the restaurant on the moon? Great food, no atmosphere.', 'Want to hear a joke about paper? Nevermind it\'s tearable.', 'Why did the coffee file a police report? It got mugged.', 'What do you call cheese that isn\'t yours? Nacho Cheese.',
        'Why couldn\'t the bicycle stand up by itself? It was two tired.', 'This graveyard looks overcrowded. People must be dying to get in there.', 'What\'s brown and sticky? A stick.', 'A furniture store keeps calling me. All I wanted was one night stand.', 'I thought about going on an all almond diet. But that iss just nuts.', 'Did you hear about the kidnapping at school? It is fine, he woke up.', 'This graveyard looks overcrowded. People must be dying to get in there.',
        'I wouldn\'t buy anything with velcro. It is a total rip off.', 'How does a penguin build its house? Igloos it together.', 'Why did the scarecrow win an award? Because he was outstanding in his field. But hay, it must run in his jeans.']

MYTHS = ['seasonal', 'hot', 'humid', 'warmer', 'bites', 'mosquitoes', 'mosquito', 'mozzie', 'hand dryers', 'hand dryer',
        'uv', 'radiation', 'sterilize', 'disinfect', 'disinfection', "thermal scanners", "security check", "detecting",
        'spraying alcohol', 'spraying chlorine', 'alcohol', 'chlorine', 'pneumonia', 'flu', 'cold', 'youth', 'young', 
        'children', 'under 50', 'ages', 'sona', 'bath', 'hamam', 'cold', 'snow', 'sanitizer', 'make my own']

def myth_busters(message):
  hot_seasonal_flu = ['seasonal', 'hot', 'humid', 'warmer']
  cold_kills_virus = ['cold', 'snow']
  sauna_bath_kill = ['sona', 'bath', 'hamam']
  animal_transmit = ['bites', 'mosquitoes', 'mosquito', 'mozzie']
  hand_dryers = ['hand dryers', 'hand dryer']
  uv_lamp = ['uv', 'radiation', 'sterilize', 'disinfect', 'disinfection']
  thermal_scanners = ["thermal scanners", "security check", "detecting"]
  make_shift_sanitizers = ['spraying alcohol', 'spraying chlorine', 'alcohol', 'chlorine', 'sanitizer', 'make my own']
  vaccines = ['pneumonia', 'flu', 'cold']
  young_old_people = ['youth', 'young', 'children', 'under 50', 'ages']


  
  if(any(keywords in message.lower() for keywords in sauna_bath_kill) and 'hot' in message.lower()):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/mb-hot-bath.tmb-1920v.png?sfvrsn=f1ebbc_1"
  elif(any(keywords in message.lower() for keywords in hot_seasonal_flu) and 'virus' in message.lower()):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/52.tmb-1920v.png?sfvrsn=862374e_1"
  elif(any(keywords in message.lower() for keywords in cold_kills_virus) and 'virus' in message.lower()):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/mb-cold-snow.tmb-1920v.png?sfvrsn=1e557ba_1"
  elif(any(keywords in message.lower() for keywords in animal_transmit)):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/mb-mosquito-bite.tmb-1920v.png?sfvrsn=a1d90f6_1"
  elif(any(keywords in message.lower() for keywords in hand_dryers)):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/mythbusters-27.tmb-1920v.png?sfvrsn=d17bc6bb_1"
  elif(any(keywords in message.lower() for keywords in uv_lamp)):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/mythbusters-31.tmb-1920v.png?sfvrsn=e5989655_1"
  elif(any(keywords in message.lower() for keywords in thermal_scanners)):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/mythbusters-25.tmb-1920v.png?sfvrsn=d3bf829c_2"
  elif(any(keywords in message.lower() for keywords in make_shift_sanitizers)):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/mythbusters-33.tmb-1920v.png?sfvrsn=47bfd0aa_2"
  elif(any(keywords in message.lower() for keywords in vaccines) and 'vaccine' in vaccines):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/web-mythbusters/11.tmb-1920v.png?sfvrsn=97f2a51e_2"
  elif('garlic' in message.lower()):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/19.tmb-1920v.png?sfvrsn=52adfc93_3"
  elif(any(keywords in message.lower() for keywords in young_old_people)):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/mythbuster-2.tmb-1920v.png?sfvrsn=635d24e5_3"
  elif('antibiotics' in message.lower()):
    return "https://www.who.int/images/default-source/health-topics/coronavirus/myth-busters/mythbuster-3.tmb-1920v.png?sfvrsn=10657e42_3" 


def wawa_get_symptoms():
  symptoms = """The most common symptoms are: 
😰Severe breathing problems (gasping, turning blue, can't talk normally)
😖Chest pain (heavy weight around or in chest)
😵Stroke (unbale to raise arm, drooping face or one sided limb weakness)
😷Soar throat
🤧Persistant coughing
🤒Fever

If you experience any of these symptoms either call your gp or in more sever cases ask me for your *emergency [country]* number  🚑"""

  return symptoms

def wawa_tell_who_recommendations():
  recommendations = """🧼👏Wash your hands frequently.
🧍↔️🧍Maintain social distancing.
🚫🤦Avoid touching eyes, nose and mouth. 
🤧Practice respiratory hygiene.
😷If you have fever, cough and difficulty breathing, seek medical care early. 
🧑‍⚕️Stay informed and follow advice given by your healthcare provider.

For more information: https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public"""

  return recommendations

def wawa_get_emergency(country):
  with open("countries.txt") as json_file:
    data = json.load(json_file)
  
  US_list = ["usa", "merica", "us", "united states of america", "america", "murica"]
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
  message = """Wawa-wee-wa 🤖. Welcome to a *fun* and *instructive* space, to get the straight facts and fun you need in this strange time.
  
I am still learning the strange human language, so my vocabulary is still limited. Type *help* to see what I understand"""

  return message

def wawa_tell_instructions():
  message = """📰Ask me to see the *latest recommendations* by the WHO to keep you safe and well informed
😂Ask me to tell you a *joke*
🖼️Ask me for a *meme*
🆕Ask me for an *update [in your country]* on how the virus is progressing e.g. *update UK*
🚑Ask me if you have an emergency for your national emergency number: *emergency [country]*
🤧Ask me about common symptoms *symptoms*
🦄Ask me about some common myths or things you might be unsure about.

To check my vocabulary ask for *help*"""

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
    country = "United States of America"
  elif (country.lower() in UK_list):
    country = "United Kingdom"
  elif (country.lower() in UAE_list):
    country = "United Arab Emirates"

  country_tolower = country.lower()

  while(True):
    if response_json['Countries'][count]['Country'].lower() == country_tolower:
      new_confirmed = response_json['Countries'][count]['NewConfirmed']
      new_deaths =  response_json['Countries'][count]['NewDeaths']
      new_recovered = response_json['Countries'][count]['NewRecovered']
      total_confirmed = response_json['Countries'][count]['TotalConfirmed']
      return wawa_update_message(new_confirmed, new_deaths, new_recovered, total_confirmed, country)
    if response_json['Countries'][count]['Country'] == "Zimbabwe":
      break
    count += 1
  return "Sorry you must have written a wrong country name."

def wawa_get_meme():
  start = int(round(time.time() * 1000))
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

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
  return send_from_directory(os.getcwd() + "/backup_memes",
                             filename)

@app.route('/upload/<filename>', methods=['GET', 'POST'])
def uploaded_file_love(filename):
  return send_from_directory(os.getcwd() + "/static/img/",
                             filename)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sms", methods=['POST'])
def whatsapp_reply():
  """
    Respond to basic message on whatsapp
  """
  msg = request.form.get('Body')

  # Start out response
  resp = MessagingResponse()

  greeting_list = ["hey", "good morning", "good evening", 'g\'day', "good morrow", "hello", "hi", "sup"]
  joke_list = ["bored", "joke", "laugh"]
  meme = ["meme", "funny picture", "bored", "boring"]
  status = ['how are you', 'whats up', 'what\'s up', 'howdy', 'what\'s new', 'how are you doing', 'how are you coping']
  sad_response = ['bad', "not well", "stressed", "angry", "sad", "pissed off", "nervous"]
  good_response = ['good', 'awesome', 'great', 'happy', 'relieved']

  #Myths
  if(any(keywords in msg.lower() for keywords in MYTHS)):
    msg = resp.message("Wawa-wee-wa 🤖. Myth busting activated.").media(myth_busters(msg))
  #Greetings
  elif (any(keywords in msg.lower() for keywords in greeting_list)):
    msg = resp.message(wawa_tell_welcome())
  #Answer
  elif(any(keywords in msg.lower() for keywords in status)):
    msg = resp.message("I am good! How are you today?")
  #Sad response
  elif(any(keywords in msg.lower() for keywords in sad_response)):
    msg = resp.message("Aww! It will get better with time. Ask me for a *joke* or *meme*, I want to cheer you up!").media('https://wawaweewabot.herokuapp.com/upload/WawaLove.png')
  #Good respone
  elif(any(keywords in msg.lower() for keywords in good_response)):
    msg = resp.message("Great to hear that!")
  #Meme
  elif (any(keywords in msg.lower() for keywords in meme)):
    try:
      image, message = wawa_get_meme()
    except urllib.error.HTTPError as e:
      print("caught")
      index = randint(1, 26)
      image, message = 'https://wawaweewabot.herokuapp.com/uploads/{}'.format(index) + '.jpg', "Here is your meme!"
    finally:
      msg = resp.message(message).media(image)
  #Joke
  elif (any(joke in msg.lower() for joke in joke_list)):
    msg = resp.message(wawa_tell_joke())
  #Update
  elif ("update" in msg.lower()):
    country = msg[7:]
    msg = resp.message(covid_api(country))
  #Instructions
  elif ("instructions" in msg.lower() or "help" in msg.lower()):
    msg = resp.message(wawa_tell_instructions())
  #Emergency Number
  elif ("emergency" in msg.lower()):
    country = msg[10:]
    print(country)
    msg = resp.message(wawa_get_emergency(country))
  #Reccomendations
  elif ("who" in msg.lower() or "recommendations" in msg.lower() or "world health organisation" in msg.lower()):
    msg = resp.message(wawa_tell_who_recommendations())
  #Symptoms
  elif('symptoms' in msg.lower() or "unwell" in msg.lower()):
    msg = resp.message(wawa_get_symptoms())
  #Default message
  else:
    msg = resp.message("""Sorry I did not catch that. Ask me for *help* to obtain my vocabulary. 

Or *emergency [your country]* if you need it.""")

  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)