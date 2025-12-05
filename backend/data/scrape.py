import requests as re
from bs4 import BeautifulSoup as bs

raw = "raw_data/pg10-images.html"

def obtain_soup(url):
  with open(url,"r",encoding="utf-8",errors="ignore") as file:
    bible = file.read()
  soup = bs(bible,features="html.parser")
  p_tag = soup.find("p")
  return p_tag

bible_soup = obtain_soup(raw)
with open("prep_data.json", "w") as file:
  file.write(bible_soup.text)
  
