from pymongo import MongoClient
from sys import argv as args
from utils import *
from datetime import date
import re

<<<<<<< HEAD
def run():
  title = args[1]
  url = args[2]
  date = args[3]
  password = args[4]
  calldb(title, url, date, password)
  
def calldb(title, url, date, password):
  client = MongoClient(f"mongodb+srv://admin:{password}@wattbot.mcfnd.mongodb.net/Stats?retryWrites=true&w=majority")
  db = client.Wattbot
  book = {'title':title,
          'url':url,
          'dateadded':date}
  res = db.Books.insert_one(book)
  print(res)
  
run()
=======
def addbook(username, password):
    db = databaseconnect(password)
    userprofile = f'https://www.wattpad.com/user/{username}'
    urls = scrapeprofile(userprofile)
    for url in urls:
        new = checkbook(url, db)
        if new:
            print("[*] Adding new book")
            info = scrapebook(url, db)
            savebook(info, db)

def scrapeprofile(url):
    resp = connect(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    print("[*] Scrape Complete")
    mydivs = list(soup.find_all('a', {"class":"send-cover-event on-story-preview cover cover-home"}))
    urls = []
    for div in mydivs:
        storyurl = re.findall('(/story/[0-9]{9}.+)">', str(div))
        url = f'https://www.wattpad.com{storyurl[0]}'
        urls.append(url)
    return urls

def checkbook(url, db):
    new = True
    col = db['Books']
    books = col.find()
    for book in books:
        if book['url'] == url:
            new = False
    return new

def scrapebook(url, db):
    data = []
    title = re.findall('/story/[0-9]{9}(.+)', str(url))
    data.append(title[0])
    data.append(url)
    data.append(date.today().strftime("%d%m%Y"))
    books = db['Books']
    res = books.find({},{'bookid':1}).sort('bookid', -1)
    for r in res:
        nextid = str(int(r['bookid'])+1)
    data.append(nextid)
    return data

def savebook(info, db):
    book = {'title':info[0],
        'url':info[1],
        'dateadded':info[2],
        'id':info[3]}
    res = db.Books.insert_one(book)
    print(res)
>>>>>>> 1ea88e4 (refined adding new works)
