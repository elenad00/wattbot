from sys import argv
from addbook import addbook
from today import gettoday
from summaries import *
# wattbot checks your profile to see if you have any new books, or have deleted any
# if you have new books, wattbot will add them to the database
username = argv[1]
password = argv[2]
addbook(username, password)
# then, wattbot will scrape today's data from all of the books you have published
# this data is then returned to you and saved to the database
db, books = gettoday(password)
# wattbot will then compare today's data to yesterdays and give you the rundown
getyesterday(books, db)
# every week, wattbot will give you your weekly stats
getthisweek(books, db)
# every month, wattbot will give you your monthly stats
getthismonth(books, db)
