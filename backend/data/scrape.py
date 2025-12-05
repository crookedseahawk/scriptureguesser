import requests as re
from bs4 import BeautifulSoup as bs

raw = "/raw_data/gutenberg_bible.html"

def obtain_soup(url):
  request = re.get(url)
  soup = bs(request.text,features="html.parser")
  return soup

bible_soup = obtain_soup(raw)
with open("prep_data.json", "w") as file:
  file.write(bible_soup[0])
  
