# wattbot
a bot for tracking wattpad engagement

## how it works
wattbot works by scraping the data from the story page of any books you want

## what data is collects
wattbot currently collects:
- reads
- votes
- parts
<<<<<<< HEAD

=======
>>>>>>> 50c2006 (edited readme)
wattbot calculates:
- average votes per part
- reads per like
- overall engagement

## why wattbot was created
wattbot was created so that reading stats can be collected and analysed in ways that make sense to those who want to deeply analyse the performance of their works

## where the data is stored
<<<<<<< HEAD
all data collected from wattbot is stored in a mongodb database

## dataflow
1. wattbot checks your profile to see if you have any new books, or have deleted any
2. if you have new books, wattbot will add them to the database
3. then, wattbot will scrape today's data from all of the books you have published
4. this data is then returned to you and saved to the database
5. wattbot will then compare today's data to yesterdays and give you the rundown
6. every week, wattbot will give you your weekly stats
7. every month, wattbot will give you your monthly stats
=======
all data collected from wattbot is stored in a mongodb database
>>>>>>> 50c2006 (edited readme)
