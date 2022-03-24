import requests
import urllib.request
from sys import argv
from urllib.parse import unquote
from bs4 import BeautifulSoup
from colored import fg, bg, attr

import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def run():
  criteria = argv[1]
  #scrapeselenium(criteria)
  searchfor()

def scrapeselenium(criteria):
  driver = webdriver.Chrome(executable_path='./chromedriver')
  url = 'https://www.wattpad.com/search/george%20russell'
  driver.get(url)

  cookies = driver.find_elements(By.ID, 'onetrust-accept-btn-handler')
  cookies[0].click()
  
  i = 15
  while i < 615:
    driver.execute_script("window.scrollTo(1,50000)")
    time.sleep(1.5)
    nextpage = driver.find_elements(By.CLASS_NAME, 'load-more')
    nextpage[0].click()
    i+=15

  sauce = driver.page_source
  driver.close()

  file = open('scrape-search.html', 'w')
  file.write(sauce)
  file.close()


def searchfor():
  resp = open('scrape-search.html', 'r')
  soup = BeautifulSoup(resp, 'html.parser')
  mydivs = list(soup.find_all('span', class_="sr-only"))
  books = []
  i = 5
  while i < len(mydivs):
    try:
      book = mydivs[i:i+10]
      title = getstrip(book[0])
      reads = int(getstrip(book[3]))
      likes = int(getstrip(book[5]))
      chapters = int(getstrip(book[7]))
      interaction = round((likes*likes)/(chapters*reads), 2)
    except ZeroDivisionError:
      interaction = 0
    except (ValueError, IndexError):
      print(i)

    if title in ['under the cover of darkness [g.r]', 'in the morning light [g.r]']:
      pink = bg('indian_red_1a') + fg('white')
      reset = attr('reset')
      title = pink + title + reset
    books.append([title, interaction])
    i+=20
  books = sorted(books,key=lambda l:l[1], reverse = True)
  for i in range(0, len(books)):
    book = books[i]
    title = unquote(book[0])
    print(f'{i+1}: {title} with a score of {book[1]}')

def getstrip(spanval):
  strippedval = str(spanval).replace('<span class="sr-only">', '').replace(',','').replace('</span>','')
  return strippedval

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
  return resp


run()