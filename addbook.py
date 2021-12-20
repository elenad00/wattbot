from pymongo import MongoClient
from sys import argv as args

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