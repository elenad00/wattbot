try:
  password = argv[1]
except Exception:
  print("[!] No Password Supplied")
  exit(1)
client = MongoClient(f"mongodb+srv://admin:{password}@wattbot.mcfnd.mongodb.net/Stats?retryWrites=true&w=majority")
db = client["Wattbot"]