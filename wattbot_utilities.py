# local imports
import s

# module imports
from argparse import ArgumentParser, Namespace
from datetime import date, datetime
from bs4 import BeautifulSoup as soup, Tag
from pymongo import MongoClient
import re
import requests
from typing import Any

class Book_Instance:
    def __init__(
        self, 
        title: Tag, 
        id: int,
        date: str,
        reads: Tag,
        likes: Tag,
        chapters: Tag
    ):
        self.id = id
        self.title = self.get_strip(title)
        self.date = date
        self.reads = self.get_strip(reads)
        self.likes = self.get_strip(likes)
        self.chapters = self.get_strip(chapters)
        
        self.avglpc = round(self.likes/self.chapters, 1)
        self.avgrpl = round(self.reads/self.likes, 2) 
        self.interaction = round(
            (self.likes*self.likes)/(self.reads*self.chapters),
            2
        )

    def get_stats(self):
        instance = {
            'bookid':self.id,
            'date':self.date,
            'reads':self.reads,
            'likes': self.likes,
            'chapters': self.chapters,
            'avglpc': self.avglpc,
            'readsperlike': self.avgrpl,
            'interaction': self.interaction
        }
        return instance
    
    def get_strip(self, spanval: Tag) -> int | str:
        span_val = str(spanval)
        regex_match = re.findall(
            "<span class=\"sr-only\">([\w\s\d\,\[\]\.]+)</span>",
            span_val
        )
        try:
            val = regex_match[0].replace(',','')
        except IndexError:
            val = span_val
        try: 
            return int(val)
        except ValueError: 
            return val
    
    def print_today(self):
        print(self.title)
        print(f'  Reads: {self.reads}\n  Likes: {self.likes}\n  Chapters: {self.chapters}')
        print(f'  Average Likes Per Chapter: {self.avglpc}')
        print(f'  Reads per Like: {self.avgrpl}')
        print(f'  Interaction Score: {self.interaction}')
        print('')
        
class Compare:
    def __init__(self, today: Book_Instance, yesterday: Book_Instance):
        self.days = self.compare_dates(today.date, yesterday.date)
        self.reads = self.calculate(today.reads, yesterday.reads)
        self.likes = self.calculate(today.likes, yesterday.likes)
        self.chapters = self.calculate(today.chapters, yesterday.chapters)
        self.lpc = self.calculate(today.avglpc, yesterday.avglpc)
        self.rpl = self.calculate(today.avgrpl, yesterday.avgrpl)
        self.int = self.calculate(today.interaction, yesterday.interaction)
    
    def calculate(self, today_value: int, yesterday_value: int) -> str:
        minus = today_value-yesterday_value
        if minus == 0:
            return '0'
        if type(minus) == float and minus>0:
            return '+'+str(round(minus, 1))
        if type(minus) == float and minus<0:
            return str(round(minus, 1))
        if minus>0:
            return '+'+str(minus)
        else:
            return str(minus)
        
    def compare_dates(self, tdy: str, ydy: str):
        today = datetime(int(tdy[4:8]),int(tdy[2:4]),int(tdy[0:2]), 0, 0)
        yesterday = datetime(int(ydy[4:8]),int(ydy[2:4]),int(ydy[0:2]), 0, 0)
        return (str(today-yesterday).split(','))[0]

    def print_comparison(self):
        print('Differences over the last', self.days)
        print(f'  Reads: {self.reads}\n  Likes: {self.likes}\n  Chapters: {self.chapters}')
        print(f'  Average Likes Per Chapter: {self.lpc}')
        print(f'  Reads per Like: {self.rpl}')
        print(f'  Interaction Score: {self.int}')
        print('')

def get_args() -> Namespace:
    args = ArgumentParser('The commands to run the script')
    args.add_argument(
        '-u', '--username', type=str, default='lazorjam',
        help='The username of the profile to scan'
    )
    args.add_argument(
        '-t', '--target', type=str, default=150000,
        help='The target reads for your books'
    )
    arguments = args.parse_args()
    return arguments

def scrape(url: str) -> soup:
    response = requests.get(url, headers=s.wattpad_header())
    formatted = soup(response.text, 'html.parser')
    return formatted

def profile_scrape(profile_url: str) -> list[str]:
    urls = list()
    stories = list(scrape(profile_url).find_all('a',{'class':"send-cover-event"}))
    for story in stories:
        url = re.findall('href="(.*)"', str(story))[0]
        urls.append(f'https://www.wattpad.com{url}')
    return urls

def database_connect() -> Any:
    client = MongoClient(s.get_mongo_url())
    database_connection = client['Wattbot']
    return database_connection

def check_books_exist(book_urls: list[str]) -> list[str]:
    saved_urls =[book['url'] for book in database_connect()['Books'].find({},{'url':1}).sort('id',1)]
    for url in book_urls:
        if url not in saved_urls:
            print("Adding new book...")
            new_book = add_book(url)
            print(f"{new_book} added to database")
        else:
            saved_urls.remove(url)
    if len(saved_urls)!=0:
        print(f"{len(saved_urls)} book/s have been deleted\n")
    return book_urls

def add_book(url: str) -> str:
    database_connection = database_connect()
    title = (re.findall('.*[0-9]{9}(.+)', str(url)))[0].replace('-',' ')
    current_highest_id = [b for b in database_connection['Books'].find().sort('id',-1)][0]['id']
    book_id = int(current_highest_id)+1
    book = {
        'title':title,
        'url':url,
        'dateadded':date.today().strftime('%d%m%Y'),
        'id':book_id
    }
    database_connection['Books'].insert_one(book)
    return title

def get_stats(url: str) -> Book_Instance:
    today = date.today().strftime("%d%m%Y")
    book_id = [book['id'] for book in database_connect()['Books'].find({'url':url},{'id':1})][0]
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

def add_instance(book: Book_Instance) -> Any:
    return database_connect()['instances'].insert_one(book.get_stats())

def get_yesterday(book: Book_Instance) -> Book_Instance:
    today = date.today().strftime('%d%m%Y')
    previous_days = database_connect()['instances'].find({'bookid':book.id},{'_id':0})
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
    
def compare_dates(today: Book_Instance, yesterday: Book_Instance):
    comp = Compare(today, yesterday)
    comp.print_comparison()
    return comp
 
def days_until(goal_reads: int, today: Book_Instance, comp: Compare):
    current_reads = int(today.reads)
    average_rpd = round(int(comp.reads)/int((comp.days).split(' ')[0]), 0)
    reads_left = goal_reads-current_reads
    if reads_left<0:
        print(f"Woo! You've already hit {goal_reads} reads")
        return True
    print(f"You're only {reads_left} reads away from your goal of {goal_reads}")
    days = int(round(reads_left/average_rpd, 0))
    print(f"That means there's only {days} day/s left!")
    print('\n---\n')
    return False
