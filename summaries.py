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

def getyesterday(bookid, db):
>>>>>>> 1ea88e4 (refined adding new works)
    print("[*] Retrieving todays data")
    today = date.today().strftime("%d%m%Y")
    tres = getvals(today, bookid, db)

    print("[*] Retrieving yesterdays data")
    yest = (date.today() - timedelta(days=1)).strftime("%d%m%Y")
    yres = getvals(yest, bookid, db)

    compare(tres, yres)

def getvals(date, bookid):
    data = db["instances"].find({'date':date, 'bookid':bookid}, {'_id':0, 'bookid':0, 'date':0})
    ints=''
    for instance in data:
        print(instance)
        ints = list(instance.values())
    try:
        return ints
    except Exception as e:
        print('[!] Error querying MongoDB')
        print(e)
        exit(1)

def compare(tod, yes):
    compdata = []
    for i in range(0, len(tod)):
        compdata.append(round(tod[i]-yes[i],1))
    print(f'[+] Value Increases:\n\tReads: {compdata[0]}\n\tLikes: {compdata[1]}\n\tChapters: {compdata[2]}')
    print(f'\tAverage Likes Per Chapter Change: {compdata[3]}')
    print(f"\tReads per Like Change: {compdata[4]}")
    print(f"\tInteraction Score Change: {compdata[5]}\n")
