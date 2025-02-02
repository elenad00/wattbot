'''
Wattbot
Written by Elena D
Created 2023

How to run:
python3 wattbot.py -u <wattpad_username> -t <target reads>
'''
# imports
import bot_utils

def main():
    cmd_args = bot_utils.get_args()
    username = cmd_args.username
    print(f"Showing results for {username}")
    book_urls = bot_utils.profile_scrape(username, "Wattpad")
    verified_book_urls = bot_utils.check_books_exist(book_urls)
    for book in verified_book_urls:
        book_class = bot_utils.get_stats(book)
        bot_utils.add_instance(book_class)
        book_class.print_today()
        yesterday_class = bot_utils.get_yesterday(book_class)
        comp = bot_utils.compare_dates(book_class, yesterday_class)
        bot_utils.days_until(int(cmd_args.target), book_class, comp)
    return True

main()