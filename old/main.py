import requests
import urllib.request
import time
import re
import numpy as np
from pymongo import MongoClient
from datetime import date, timedelta
from requests.structures import CaseInsensitiveDict
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
from sys import argv

# step one:
#    get arguments from command line
def run():
  username = argv[1]
  password = argv[2]
  db = databaseconnect(password)
  profilescrape(username, db)
  books = getallbooks(db)
  for book in books:
    gettoday(db,book)
    getyesterday(db, book)
    getlastweek(db, book)
    #getlastmonth(db, book)

# step two:
#   connect to database
def databaseconnect(password):
  client = MongoClient(f"mongodb+srv://admin:{password}@wattbot.mcfnd.mongodb.net/Stats?retryWrites=true&w=majority")
  db = client.Wattbot
  return db

#step three:
#   check to see if there have been any new books on the user's account
def profilescrape(username, db):
  profilebooks = []
  userprofile = f'https://www.wattpad.com/user/{username}'
  resp = connect(userprofile)
  soup = BeautifulSoup(connect(userprofile).text, 'html.parser')
  mydivs = list(soup.find_all('a', {"class":"send-cover-event on-story-preview cover cover-home"}))
  for div in mydivs:
    storyurl = re.findall('(/story/[0-9]{9}.+)">', str(div))
    url = f'https://www.wattpad.com{storyurl[0]}'
    profilebooks.append(url)
  
  dburls = []
  books = getallbooks(db)
  for book in books:
    dburls.append(book['url'])

  for url in profilebooks:
    if url not in dburls:
      print("[*] Adding new book")
      title = (re.findall('/story/[0-9]{9}(.+)', str(url)))[0].replace('-',' ')
      books = db['Books']
      res = books.find({},{'bookid':1}).sort('bookid', -1)
      for r in res:
        nextid = str(int(r['bookid'])+1)
      book = {'title':title,
        'url':url,
        'dateadded':date.today().strftime("%d%m%Y"),
        'id':nextid}
      res = db.Books.insert_one(book)

#step four:
#   get todays data

def gettoday(db, book):
  today = date.today().strftime("%d%m%Y")
  run = False
  instances = getallinstances(db)
  print(f"[*] Getting results for {book['title']}")
  for instance in instances:
    if instance['date'] == today and instance['bookid'] == book['id']:
      run = True
  if not run:
    stats = scrape(book['url'])
    appenddb(book['id'], stats, db)

#step five:
#   compare to yesterday
def getyesterday(db, book):
  getdata(2, book, db)

#step six:
#   compare to last week
def getlastweek(db, book):
  getdata(7, book, db)

#step seven:
#   compare to last month
def getlastmonth(db, book):
  getdata(28, book, db)

# misc resources
def connect(url):
  headers = CaseInsensitiveDict()
  headers["Cookie"] = "RT=r=https%3A%2F%2Fwww.wattpad.com%2Flogin&ul=1637322875469; _fbp=fb.1.1637320628336.1837372595; pbjs-unifiedid=%7B%22TDID%22%3A%22cb841ae8-a2a3-4aa2-a6a7-00f5a1c11fae%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222021-11-19T11%3A48%3A22%22%7D; OptanonConsent=isIABGlobal=false&datestamp=Fri+Nov+19+2021+11%3A54%3A26+GMT%2B0000+(GMT)&version=6.10.0&hosts=&consentId=36f0e37b-c47d-4850-8a6b-867b55aa6d17&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1%2CSTACK42%3A1&AwaitingReconsent=false&geolocation=GB%3BENG; _ga=GA1.2.1750512678.1637320628; _ga_FNDTZ0MZDQ=GS1.1.1637320628.1.1.1637322866.0; _gat_UA-886196-1=1; _gid=GA1.2.1855559847.1637320628; sn__time=j%3Anull; te_session_id=1637320628147; _pubcid=e2fdcd22-7176-45dd-b0f6-9a6161b515f6; fb_login=1; fs__exp=2; _pbeb_=1; _pbjs_userid_consent_data=3524755945110770; _ukpb_=1; adMetrics=0; cto_bidid=iX3coV9BNGZpWVZWQ0h6RDQwdCUyRmElMkJpSVl3VnN4dkJoaHZKbFdYWUJPZFpKemhIUWcwJTJCbVZsSVlQV1hKYzd0VWZ1SWp6dTI0ZTlMdiUyRk5JZ3YyTWMyaWttZHR3JTNEJTNE; cto_bundle=Wr0R5F84bXYxRWwyakFPVVdYcWVydm5veGdWVHk4WWNWa1NiOEh2eWlqWmd5U0pOQmVpMyUyQkZ2ZVclMkJXTEtmRXRKSnB6JTJCVTE5cVZXT3ZQSnFEdlZ2QjE0cyUyRm1UQU1BVXNRM2dmYzFFMyUyQktzZFppOXdXbWJ5RWU0JTJCRDhwalhBNW5GZmJUJTJG; dpr=2; tz=0; _dd_s=logs=1&id=5cc178df-093f-48e8-a0a4-0242b28be09b&created=1637322500440&expire=1637323764618; hc=0; isStaff=1; signupFrom=story_reading; _pubcid=e2fdcd22-7176-45dd-b0f6-9a6161b515f6; cto_bundle=vBrX4V84bXYxRWwyakFPVVdYcWVydm5veGdVa3NuYk5HTzRvSUQzRDFhbW1vQ0xtbmhkSGJuUHQ3WDliMERYSmtHMXc0NGlPSXV4OHRwTFM5RGpZRFVGJTJGNXhKV0RlNG9GcXA2ZURwJTJCenJQRmFzaWlENzNDQlJTcFNJRm80QnNtazNwN3Q; seen-wallet-onboard=1; OptanonAlertBoxClosed=2021-11-19T11:19:15.856Z; eupubconsent-v2=CPP607bPP607bAcABBENB2CsAP_AAH_AAChQIXtf_X__b3_j-_59f_t0eY1P9_7_v-0zjhfdt-8N2f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7__8___z_v-v_v____f_7-3_3__5_X---_e_V399zLv9____39nP___9v-_9-CF4BJhqXkAXYljgybRpVCiBGFYSHQCgAooBhaIrCBlcFOyuAj1hCwAQmoCMCIEGIKMGAQACAQBIREBIAeCARAEQCAAEAKkBCAAjYBBYAWBgEAAoBoWIEUAQgSEGRwVHKYEBEi0UE9lYAlB3saYQhllgBQKP6KjARKEECwMhIWDmOAJAS4WSBZgAAAAA.f_gAD_gAAAAA; __qca=P0-1623306800-1637320682718; panoramaId_expiry=1637407029705; _lr_env_src_ats=false; _lr_retry_request=true; AMP_TOKEN=%24NOT_FOUND; ff=1; lang=1; locale=en_US; wp_id=3f64cb16-57fa-489a-916e-1b344d0e15a8"
  headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  headers["If-None-Match"] = '"W/"26446-7iMCjFRAk1ZfCEKUGR492nL/+lQ""'
  headers["Host"] = "www.wattpad.com"
  headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"
  headers["Accept-Language"] = "en-gb"
  headers["Accept-Encoding"] = "gzip, deflate, br"
  headers["Connection"] = "keep-alive"
  resp = requests.get(url, headers=headers)
  if resp.status_code != 200:
    print("[!] Could not connect to Wattpad")
    exit(1)
  return resp

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
  interaction = round((likes*likes)/(reads*chapters), 2)
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

def getallbooks(db):
    col = db["Books"]
    books = col.find()
    return books

def getallinstances(db):
    col = db["instances"]
    instances = col.find()
    return instances

def getdata(max, book, db):
    bookid = book['id']
    res = []
    for i in range(1,max+1):
        data = db["instances"].find({'bookid':bookid}, {'_id':0})
        data = list(data)
        res.append(data[-i])
    first = res[0]
    last = res[-1]
    compdata = [first['bookid'],
        first['reads']-last['reads'],
        first['likes']-last['likes'],
        first['chapters']-last['chapters'],
        round(first['avglpc']-last['avglpc'], 1),
        first['readsperlike']-last['readsperlike'],
        round(first['interaction']-last['interaction'],1)
    ]
    date = last["date"]
    date = f"{date[0:2]}-{date[2:4]}-{date[4::]}"
    print(f'[+] Value changes since {date}:')
    print(f'\tReads: {compdata[1]}\n\tLikes: {compdata[2]}\n\tChapters: {compdata[3]}')
    print(f'\tAverage Likes Per Chapter Change: {compdata[4]}')
    print(f"\tReads per Like Change: {compdata[5]}")
    print(f"\tInteraction Score Change: {compdata[6]}\n")

run()
