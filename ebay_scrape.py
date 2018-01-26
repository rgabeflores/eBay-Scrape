from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from pprint import PrettyPrinter

from modules import ux
from modules.statistics import mean, median, mode, variance, std_dev
from api import spreadsheet as ss

'''
    TO-DO
    • Optimize with generators, decorators, & context managers
    • Implement cleaner exception handling (try,except,else,finally)
'''

# Retrieve API key via text file
APP_ID = ""
api = ""

OPTIONS = (
    "New Search",
    "View Spreadsheet",
)


def call_ebay_api(keywords=None):
    '''
            Uses the ebaysdk library to call eBay's API
    '''
    api = finding(appid=APP_ID, config_file=None)
    api_request = {'keywords': keywords}
    response = api.execute('findItemsByKeywords', api_request)
    soup = BeautifulSoup(response.content, 'lxml')

    items = soup.find_all('item')

    return items


def new_search():
    user_input = input("\n\n\tEnter keywords: ").strip()

    items = (item for item in call_ebay_api(keywords=user_input))

    prices = [float(item.currentprice.string) for item in items]

    if len(prices) > 0:
        _high = max(prices)
        _low = min(prices)
        _mean = round(mean(prices), 2)
        _median = median(prices)
        _mode = mode(prices)
        _variance = round(variance(prices, average=_mean), 2)
        _std_dev = round(std_dev(prices, average=_mean, var=_variance), 2)

        print("\t" + ("_____" * 10) + "\n")
        print("\tFound " + str(len(prices)) + " different prices.")
        print("\t" + ("_____" * 10) + "\n")

        print("\tHigh:", _high)
        print("\tLow:", _low)
        print("\tMean:", _mean)
        print("\tMedian:", _median)
        print("\tMode:", _mode)
        print("\tVariance:", _variance)
        print("\tStandard Deviation:", _std_dev)

        print("\t" + ("_____" * 10) + "\n")
        print("\tApproximately 68%% of offers are between", round(_mean - _std_dev, 2), "and", round(_mean + _std_dev, 2))
        print("\tApproximately 95%% of offers are between", round(_mean - (2 * _std_dev), 2), "and", round(_mean + (2 * _std_dev), 2))
        print("\tApproximately 99.7%% of offers are between", round(_mean - (3 * _std_dev), 2), "and", round(_mean + (3 * _std_dev), 2))
        print("\t" + ("_____" * 10) + "\n")

        print("\tAppending to Spreadsheet...")
        ss.insert_record([user_input.upper(), len(prices), _high, _low, _mean, _median, _mode, _variance, _std_dev], ss.get_row_count() + 1)
        print("\tFinished.")

    else:
        print("\t" + ("_____" * 10) + "\n")
        print("\tNo results were found.")
        print("\t" + ("_____" * 10) + "\n")

    print("\n")


def view_spreadsheet():

    pp = PrettyPrinter()

    pp.pprint(ss.get_records())

    print("\n")


def main():

    global APP_ID

    try:
        with open("key.txt", 'r') as f:
            APP_ID = f.readline().strip()

    except FileNotFoundError as e:
        print("\n\tA text file containing the API key must be present and in the working directory.\n")
        return

    def main_loop():
        choice = ux.get_user_choice(OPTIONS)

        if choice == 1:
            new_search()
        elif choice == 2:
            view_spreadsheet()

    ux.to_continue(main_loop)


if __name__ == "__main__":
    main()
