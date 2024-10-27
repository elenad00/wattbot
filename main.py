'''
Wattbot
Written by Elena D
Created 2023

How to run:
python3 main.py -u <wattpad_username> -t <target reads>
'''
# imports
import wattbot_utilities as wattbot_utils

def main():
    cmd_args = wattbot_utils.get_args()
    username = cmd_args.username
    print(f"Showing results for {username}")
    book_urls = wattbot_utils.profile_scrape(f'https://www.wattpad.com/user/{username}')
    verified_book_urls = wattbot_utils.check_books_exist(book_urls)
    for book in verified_book_urls:
        book_class = wattbot_utils.get_stats(book)
        wattbot_utils.add_instance(book_class)
        book_class.print_today()
        yesterday_class = wattbot_utils.get_yesterday(book_class)
        comp = wattbot_utils.compare_dates(book_class, yesterday_class)
        wattbot_utils.days_until(int(cmd_args.target), book_class, comp)
    return True

main()