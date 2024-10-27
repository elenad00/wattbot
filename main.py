'''
Wattbot 2.0
Written by Elena D
25/10/2023

How to run:
python3 main.py -u <wattpad_username> -t <target reads>
'''
# imports
from wattbot_2.wattbot_utilities import *

ARGS = get_args()

def main():
    print('Showing results for',ARGS.username)
    book_urls = profile_scrape(f'https://www.wattpad.com/user/{ARGS.username}')
    # connect to the database
    # check all books exists
    book_urls = check_books_exist(book_urls)
    # get today's stats
    for book in book_urls:
        # get today's stats for each book
        book_class = get_stats(book)
        add_today = add_instance(book_class)
        book_class.print_today()
        # compare to yesterday
        yesterday_class = get_yesterday(book_class)
        comp = compare_dates(book_class, yesterday_class)
        # get days until target reads
        days = days_until(int(ARGS.target), book_class, comp)
    return True

main()