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
from plotter import plot

<<<<<<< HEAD
def getyesterday(bookid, db):
>>>>>>> 1ea88e4 (refined adding new works)
=======
def getyesterday(books, db):
<<<<<<< HEAD
>>>>>>> 368042a (added weekly and monthly summaries)
    print("[*] Retrieving todays data")
    getdata(2, books, db, 1)
=======
    print("[*] Comparing todays data")
    data = getdata(2, books, db)
>>>>>>> bcae140 (adding error checking)

def getthisweek(books, db):
    print("[*] Retrieving this weeks data")
    data = getdata(7, books, db)

def getthismonth(books, db):
    print("[*] Retrieving this months data")
    data = getdata(28, books, db)

def getdata(x, books, db):
    days = []
    for i in range(0,x):
        days.append((date.today() - timedelta(days=i)).strftime("%d%m%Y"))

    for book in books:
        res = []
        bookid = book['id']
        for day in days:
            res.append(getvals(day, bookid, db))
        compdata = [res[0][0], res[0][1]-res[-1][1], res[0][2]-res[-1][2], res[0][3]-res[-1][3], res[0][4]-res[-1][4], res[0][5]-res[-1][5], round(res[0][6]-res[-1][6],1)]
        compare(compdata)
        reads,likes,chapters,alpc,rpc,isc = [], [],[],[],[],[]
        for i in range(0,x):
            reads.append(res[i][1])
            likes.append(res[i][2])
            chapters.append(res[i][3])
            alpc.append(res[i][4])
            rpc.append(res[i][5])
            isc.append(res[i][6])
        plot([reads,likes,chapters,alpc,rpc,isc])


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

def compare(compdata):
    print(f'[+] Value Increases for book {compdata[0]}:\n\tReads: {compdata[1]}\n\tLikes: {compdata[2]}\n\tChapters: {compdata[3]}')
    print(f'\tAverage Likes Per Chapter Change: {compdata[4]}')
    print(f"\tReads per Like Change: {compdata[5]}")
    print(f"\tInteraction Score Change: {compdata[6]}\n")
