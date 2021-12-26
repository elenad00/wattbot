import time
from datetime import date
from bs4 import BeautifulSoup as bs
from utils import connect
import re

def gettoday(db):
    today = getdate()
    runtoday = db["instances"].find({'date':today})
    books = db["Books"].find()
    try:
        if runtoday[0]:
            print("[!] Process already run today")
            return books
    except Exception:
        for book in books:
            stats = scrape(book['url'])
            appenddb(book['id'], stats, db)

def getdate():
    return date.today().strftime("%d%m%Y")

def scrape(url):
  soup = bs(connect(url).text, 'html.parser')
  mydivs = list(soup.find_all("span", {"class": "sr-only"}))
  vals = []
  for div in mydivs:
      val = re.findall('[A-Za-z ]{6}([0-9,]+)', str(div))
      if len(val) > 0 and int(val[0].replace(',','')) not in vals and val[0] != ',':
          val = int(val[0].replace(',',''))
          vals.append(val)
  reads = vals[0]
  likes = vals[1]
  chapters = vals[2]
  lpc = round(likes/chapters, 1)
  rat = round(reads/likes)
  interaction = round(likes/reads/chapters*10000, 1)
  return (getdate(), reads, likes, chapters, lpc, rat, interaction)

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
