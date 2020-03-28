import io
from PIL import Image
import os
import hashlib
import requests
import csv
import time
from bs4 import BeautifulSoup as soup
import random

def persist_image(folder_path:str, url:str):
  try:
    image_content = requests.get(url).content

  except Exception as e:
    print(f"ERROR - Could not download {url} - {e}")

  try:
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
    with open(file_path, 'wb') as f:
      image.save(f, "JPEG", quality=85)
    print(f"SUCCESS - saved {url} - as {file_path}")
  except Exception as e:
    print(f"ERROR - Could not save {url} - {e}")

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

  while (counter <= 50 and page_number < 3):
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

      if (counter == 20):
        image = random.choice(images)
        message = random.choice(messages)

        return image, message
    
    page_number += 1

    next_button = soup_page.find("span", class_="next-button")
    next_page_link = next_button.find("a").attrs['href']
    page = requests.get(next_page_link, headers=headers)
    soup_page = soup(page.text, 'html.parser')

  image = random.choice(images)
  message = random.choice(messages)

  return image, message

image, message = get_image()
print(image)
print(message)