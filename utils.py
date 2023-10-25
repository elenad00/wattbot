# utils.py
# local imports
import s
from classes import Book_Instance, Compare
# module imports
from argparse import ArgumentParser
from datetime import date
from bs4 import BeautifulSoup as soup
from pymongo import MongoClient
import re
import requests

def get_args():
    args = ArgumentParser('The commands to run the script')
    args.add_argument(
        '-u', '--username', type=str, default='lazorjam',
        help='The username of the profile to scan'
    )
    args.add_argument(
        '-t', '--target', type=str, default=150000,
        help='The target reads for your books'
    )
    return args.parse_args()

def scrape(url):
    response = requests.get(url, headers=s.wattpad_header())
    formatted = soup(response.text, 'html.parser')
    return formatted

def profile_scrape(profile_url):
    urls=[]
    stories = list(scrape(profile_url).find_all('a',{'class':"send-cover-event"}))
    for story in stories:
        url = re.findall('href="(.*)"', str(story))[0]
        urls.append('https://www.wattpad.com'+url)
    return urls

def database_connect():
    client = MongoClient(s.get_mongo_url())
    conn = client['Wattbot']
    return conn

def check_books_exist(book_urls):
    saved_urls =[book['url'] for book in CONN['Books'].find({},{'url':1}).sort('id',1)]
    for url in book_urls:
        if url not in saved_urls:
            print("Adding new book...")
            new_book = add_book(url)
            print(new_book,'added to database')
        else:
            saved_urls.remove(url)
    if len(saved_urls)!=0:
        print(len(saved_urls),"book/s have been deleted\n")
    return book_urls

def add_book(url):
    title = (re.findall('.*[0-9]{9}(.+)', str(url)))[0].replace('-',' ')
    current_highest_id = [b for b in CONN['Books'].find().sort('id',-1)][0]['id']
    book_id = int(current_highest_id)+1
    book = {
        'title':title,
        'url':url,
        'dateadded':date.today().strftime('%d%m%Y'),
        'id':book_id
    }
    res = CONN['Books'].insert_one(book)
    return title

def get_stats(url):
    today = date.today().strftime("%d%m%Y")
    book_id = [book['id'] for book in CONN['Books'].find({'url':url},{'id':1})][0]
    
    formatted = scrape(url)
    book_elements = list(formatted.find_all('span',{'class':'sr-only'}))
    book = Book_Instance(
        id = book_id,
        title=book_elements[0],
        date=today,
        reads=book_elements[2],
        likes=book_elements[4],
        chapters=book_elements[6]
    )
    return book

def add_instance(book):
    return CONN['Instances'].insert_one(book.get_stats())

def get_yesterday(book):
    today=date.today().strftime('%d%m%Y')
    previous_days = CONN['instances'].find({'bookid':book.id},{'_id':0})
    yesterday = [day for day in previous_days.sort('reads',-1) if day['date']!=today][0]
    yesterday_class = Book_Instance(
        title=book.title,
        id=book.id,
        date=yesterday['date'],
        reads=yesterday['reads'],
        likes=yesterday['likes'],
        chapters=yesterday['chapters']
    )
    return yesterday_class
    
def compare_dates(today, yesterday):
    comp = Compare(today, yesterday)
    comp.print_comparison()
    return comp
 
def days_until(goal_reads, today, comp):
    current_reads = int(today.reads)
    average_rpd = round(int(comp.reads)/int((comp.days).split(' ')[0]), 0)
    reads_left = goal_reads-current_reads
    if reads_left<0:
        print("Woo! You've already hit",goal_reads,"reads")
        return True
    print("You're only",reads_left,'reads away from your goal of',goal_reads)
    days=round(reads_left/average_rpd,0)
    print("That means there's only",int(days),"day/s left!")
    print('\n---\n')
    return False

CONN = database_connect()