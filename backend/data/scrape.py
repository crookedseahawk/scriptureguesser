import requests as re
from bs4 import BeautifulSoup as bs

raw = "raw_data/pg10-images.html"

def obtain_soup(url):
  with open(url,"r",encoding="utf-8",errors="ignore") as file:
    bible = file.read()
  soup = bs(bible,features="html.parser")
  div_tag = soup.find_all("div")
  return div_tag

bible_soup = obtain_soup(raw)
with open("prep_data/prep.csv", "w") as file:
  for b in bible_soup[4:]:
    file.write(b.text)
  
