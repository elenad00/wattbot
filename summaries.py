<<<<<<< HEAD
try:
  password = argv[1]
except Exception:
  print("[!] No Password Supplied")
  exit(1)
client = MongoClient(f"mongodb+srv://admin:{password}@wattbot.mcfnd.mongodb.net/Stats?retryWrites=true&w=majority")
db = client["Wattbot"]
print("[-] Connected to MongoDB")

def getyesterday(bookid):
=======
from pymongo import MongoClient
from datetime import date, timedelta
from sys import argv

<<<<<<< HEAD
def getyesterday(bookid, db):
>>>>>>> 1ea88e4 (refined adding new works)
=======
def getyesterday(books, db):
>>>>>>> 368042a (added weekly and monthly summaries)
    print("[*] Retrieving todays data")
    getdata(2, books, db, 1)

def getdata(x, books, db, y):
    days = []
    for i in range(0,x,y):
        days.append((date.today() - timedelta(days=i)).strftime("%d%m%Y"))
    for book in books:
        res = []
        bookid = book['id']
        for day in days:
            res.append(getvals(day, bookid, db))
        if (len(res[0]) and len(res[1]))>1:
            compare(res, y)
        else:
            print("[!] Not enough data available")

def getvals(date, bookid, db):
    data = db["instances"].find({'date':date, 'bookid':bookid}, {'_id':0, 'date':0})
    ints=''
    for instance in data:
        ints = list(instance.values())
    try:
        return ints
    except Exception as e:
        print('[!] Error querying MongoDB')
        print(e)
        exit(1)

def compare(data, y):
    compdata = []
    for i in range(0, len(data)-1):
        val = []
        for z in range(0, len(data[i])):
            if z != 0:
                val.append(round(data[i][z]-data[i+1][z],1))
            else:
                val.append(data[i][z])
        compdata.append(val)
        print(f'[+] Value Increases for book {compdata[i][0]}:\n\tReads: {compdata[i][1]}\n\tLikes: {compdata[i][2]}\n\tChapters: {compdata[i][3]}')
        print(f'\tAverage Likes Per Chapter Change: {compdata[i][4]}')
        print(f"\tReads per Like Change: {compdata[i][5]}")
        print(f"\tInteraction Score Change: {compdata[i][6]}\n")

def getthisweek(books, db):
    print("[*] Retrieving this weeks data")
    getdata(7, books, db, 6)

def getthismonth(books, db):
    print("[*] Retrieving this months data")
    getdata(28, books, db, 27)
