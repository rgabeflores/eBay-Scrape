from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
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

    prices = [float(item.currentprice.string) for item in call_ebay_api(keywords=user_input)]

    if len(prices) > 0:
        results = {
            'HIGH': max(prices),
            'LOW': min(prices),
            'MEAN': round(mean(prices), 2),
            'MEDIAN': median(prices),
            'MODE': mode(prices),
            # 'VARIANCE': round(variance(prices), 2),
            'STANDARD DEVIATION': round(std_dev(prices), 2)
        }

        print("\t" + ("_____" * 10) + "\n")
        print("\tFound " + str(len(prices)) + " different prices.")
        print("\t" + ("_____" * 10) + "\n")

        for key, value in results.items():
            print('\t{}: {}'.format(key, value))

        print("\t" + ("_____" * 10) + "\n")
        print("\tApproximately 68%% of offers are between", round(results['MEAN'] - results['STANDARD DEVIATION'], 2), "and", round(results['MEAN'] + results['STANDARD DEVIATION'], 2))
        print("\tApproximately 95%% of offers are between", round(results['MEAN'] - (2 * results['STANDARD DEVIATION']), 2), "and", round(results['MEAN'] + (2 * results['STANDARD DEVIATION']), 2))
        print("\tApproximately 99.7%% of offers are between", round(results['MEAN'] - (3 * results['STANDARD DEVIATION']), 2), "and", round(results['MEAN'] + (3 * results['STANDARD DEVIATION']), 2))
        print("\t" + ("_____" * 10) + "\n")

        plt.title('Prices')
        x = [y for y in range(len(prices))]
        plt.plot(x, prices, '-', color='b')
        for key, value in results.items():
            plt.plot(x, [value for i in range(len(prices))], '-', label=key)
        plt.legend()
        plt.show()

        print("\tAppending to Spreadsheet...")
        ss.insert_record([user_input.upper(), len(prices), results['HIGH'], results['LOW'], results['MEAN'], results['MEDIAN'], results['MODE'], results['VARIANCE'], results['STANDARD DEVIATION']], ss.get_row_count() + 1)
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
        with open("../key.txt", 'r') as f:
            APP_ID = f.readline().strip()

    except FileNotFoundError as e:
        print("\n\tA text file containing the API key must be present and in the working directory.\n")
        return
    print(APP_ID)

    def main_loop():
        choice = ux.get_user_choice(OPTIONS)

        if choice == 1:
            new_search()
        elif choice == 2:
            view_spreadsheet()

    ux.to_continue(main_loop)


if __name__ == "__main__":
    main()
