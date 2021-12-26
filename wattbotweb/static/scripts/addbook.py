from pymongo import MongoClient
from sys import argv as args
from utils import connect
from bs4 import BeautifulSoup
from datetime import date
import re

def checkbooks(username, db):
    userprofile = f'https://www.wattpad.com/user/{username}'
    soup = BeautifulSoup(connect(userprofile).text, 'html.parser')
    mydivs = list(soup.find_all('a', {"class":"send-cover-event on-story-preview cover cover-home"}))
    urls = []
    for div in mydivs:
        storyurl = re.findall('(/story/[0-9]{9}.+)">', str(div))
        url = f'https://www.wattpad.com{storyurl[0]}'
        urls.append(url)

    for url in urls:
        new = True
        col = db['Books']
        books = col.find()
        for book in books:
            if book['url'] == url:
                new = False
        if new:
            title = re.findall('/story/[0-9]{9}(.+)', str(url))
            res = db['Books'].find({},{'bookid':1}).sort('bookid', -1)
            id = str(int(res[0]['bookid'])+1)
            book = {'title':title[0],'url':url,'dateadded':date.today().strftime("%d%m%Y"),'id':id}
            res = db['Books'].insert_one(book)
