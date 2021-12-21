import requests
from requests.structures import CaseInsensitiveDict
import urllib.request
import time
from sys import argv
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient
from summaries import *
from utils import *

def scrape(url):
  resp = connect(url)
  soup = BeautifulSoup(resp.text, 'html.parser')
  print("[*] Scrape Complete")
  mydivs = list(soup.find_all("span", {"class": "sr-only"}))
  reads = getstrip(mydivs[2])
  likes = getstrip(mydivs[4])
  chapters = getstrip(mydivs[6])
  print(f'[+] Current values:\n\tReads: {reads}\n\tLikes: {likes}\n\tChapters: {chapters}')
  lpc = round(likes/chapters, 1)
  print(f'\tAverage Likes Per Chapter: {lpc}')
  rat = round(reads/likes)
  print(f"\tReads per Like: {rat}")
  interaction = round(likes/reads/chapters*10000, 1)
  print(f"\tInteraction Score: {interaction}\n")
  today = date.today()
  today = today.strftime("%d%m%Y")
  return (today, reads, likes, chapters, lpc, rat, interaction)

def getstrip(spanval):
    strippedval = int(str(spanval).replace('<span class="sr-only">', '').replace(',','').replace('</span>',''))
    return strippedval

def appenddb(bookid, stats, db):
  instance = {'bookid':bookid,
    'date':stats[0],
    'reads':stats[1],
    'likes': stats[2],
    'chapters': stats[3],
    'avglpc': stats[4],
    'readsperlike': stats[5],
    'interaction': stats[6]
  }
  res = db.instances.insert_one(instance)
  print(res)

def gettoday(password):
    client = MongoClient(f"mongodb+srv://admin:{password}@wattbot.mcfnd.mongodb.net/Stats?retryWrites=true&w=majority")
    db = client["Wattbot"]
    col = db["instances"]
    today = date.today().strftime("%d%m%Y")
    books = col.find({'date':today})
    for book in books:
        if book['date'] == today:
            print('[!] Query has already been run today')
            exit(1)
    col = db["Books"]
    books = col.find()
    for book in books:
        print(f"[*] Getting results for {book['title']}")
        stats = scrape(book['url'])
        appenddb(book['id'], stats, db)
        getyesterday(book['id'])
