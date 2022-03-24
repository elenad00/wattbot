# wattbot 2.0 by elena day
# 23-03-2022

from sys import argv
from bs4 import BeautifulSoup as bs
from headers import wattpadheader
from pymongo import MongoClient
from datetime import date, timedelta

import requests, urllib.request, re

class Book:
  def __init__(self, t, u, d, i):
    self.title = t
    self.url = u 
    self.date = d
    self.id = i

class Cmp:
  def __init__(self, id, date, reads, likes, chapters, lpc, rpl, int):
    self.date = date
    self.reads = reads
    self.likes = likes
    self.chapters = chapters
    self.avglpc = lpc
    self.avgrpl = rpl
    self.interaction = int

class Instance:
  def __init__(self, id, date, reads, likes, chapters):
    self.id = id
    self.date = date
    self.reads = reads
    self.likes = likes
    self.chapters = chapters
    self.avglpc = round(likes/chapters, 1)
    self.avgrpl = round(reads/likes) 
    self.interaction = round((likes*likes)/(reads*chapters),2)

  def getstats(self):
    instance = {'bookid':self.id,
    'date':self.date,
    'reads':self.reads,
    'likes': self.likes,
    'chapters': self.chapters,
    'avglpc': self.avglpc,
    'readsperlike': self.avgrpl,
    'interaction': self.interaction
    }
    return instance

def main():
  # 1: get the books from a user's profile
  profilebooks = profilescrape(argv[1])
  # 2: see if any of these books are new
  dbbooks = []
  for book in databaseconnect().Books.find({},{'url':1}):
    dbbooks.append(book['url'])
  if len(profilebooks) != dbbooks:
    cmpbooks(profilebooks, dbbooks)
  # 3: get todays results
  allbooks = getallbooks()
  if len(allbooks) == 0:
    print("Already run today")
    exit(0)
  for book in allbooks:
    print(book.id)
    printres(book)
    try:
      yesterday(book)
    except IndexError:
      print('[!] Not enough data to compare')
  
# ------------- add books --------------- # 

def profilescrape(username):
  profilebooks = []
  userprofile = f'https://www.wattpad.com/user/{username}'
  resp = requests.get(userprofile, headers=wattpadheader())
  soup = bs(resp.text, 'html.parser')
  mydivs = list(soup.find_all('a', {"class":"send-cover-event"}))
  for div in mydivs:
    storyurl = re.findall('(/story/[0-9]{9}.+)">', str(div))
    url = f'https://www.wattpad.com{storyurl[0]}'
    profilebooks.append(url)
  return profilebooks

def cmpbooks(profile, db):
  newbooks = list(set(profile) - set(db))
  for url in newbooks:
    addbook(url)

def addbook(url):
  title = (re.findall('/story/[0-9]{9}(.+)', str(url)))[0].replace('-',' ')
  cid = databaseconnect().Books.find_one(sort = [('id', -1)])
  nid = int(cid['id'])+1
  book = {'title':title,
    'url':url,
    'dateadded':date.today().strftime("%d%m%Y"),
    'id':nid}
  res = databaseconnect().Books.insert_one(book)

# --------------------------------------- #
# --------------- get today ------------- #
def getallbooks():
  stats = []
  books = databaseconnect().Books.find({},{'id':1, 'url':1})
  for book in books:
    today = date.today().strftime("%d%m%Y")
    runtoday = databaseconnect().instances.find_one({'date':today, 'bookid':book['id']},{'bookid':1})
    if not runtoday:
      url = book['url']
      today = scrape(book['id'], url)
      stats.append(today)
      res = databaseconnect().instances.insert_one(today.getstats())
  return stats

def scrape(id, url):
  resp = requests.get(url, headers=wattpadheader())
  soup = bs(resp.text, 'html.parser')
  mydivs = list(soup.find_all("span", {"class": "sr-only"}))
  book = Instance(id, date.today().strftime("%d%m%Y"), getstrip(mydivs[2]), getstrip(mydivs[4]), getstrip(mydivs[6]))
  return book

def getstrip(spanval):
  strippedval = int(str(spanval).replace('<span class="sr-only">', '').replace(',','').replace('</span>',''))
  return strippedval
# --------------------------------------- #
# ------------- get yesterday ----------- #
def yesterday(today):
  bookid = today.id
  data = databaseconnect().instances.find({'bookid':bookid}, {'_id':0})
  data = list(data.sort('reads', -1).limit(1))[0]
  yesterday = Instance(data['bookid'], data['date'], data['reads'], data['likes'], data['chapters'])
  date = yesterday.date
  date = f"{date[0:2]}-{date[2:4]}-{date[4::]}"
  comp = Cmp(0, date, today.reads-yesterday.reads, today.likes-yesterday.likes, today.chapters-yesterday.chapters, round(today.avglpc-yesterday.avglpc, 1), today.avgrpl-yesterday.avgrpl, round(today.interaction-yesterday.interaction,1))
  print(f'[+] Value changes since {comp.date}:')
  printres(comp)

# --------------------------------------- #
# ---------------- extras --------------- #

def printres(res):
  print(f'\tReads: {res.reads}\n\tLikes: {res.likes}\n\tChapters: {res.chapters}')
  print(f'\tAverage Likes Per Chapter: {res.avglpc}')
  print(f"\tReads per Like: {res.avgrpl}")
  print(f"\tInteraction Score: {res.interaction}\n")

def databaseconnect():
  uri = f"mongodb+srv://admin:{argv[2]}@wattbot.mcfnd.mongodb.net"
  db = MongoClient(uri).Wattbot
  return db

main()