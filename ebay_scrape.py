from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup

import ux
import statistics as stats
import spreadsheet as ss

'''
	• Requests a keyword search through eBay API w/ ebaysdk
	• Runs statistical analysis on the results
	• Appends statistical data to a Google Drive spreadsheet via Google Sheets API
'''

# INSERT API KEY HERE 
APP_ID = "GabrielF-Scraper-PRD-4134e8f72-f88173a5"

OPTIONS = (
	"New Search",
	"View Spreadsheet",
	)

def call_ebay_api(keywords=None):
	'''
		Uses the ebaysdk library to call eBay's API
	'''
	api = finding(appid=APP_ID, config_file=None)
	api_request = { 'keywords': keywords }
	response = api.execute('findItemsByKeywords', api_request)
	soup = BeautifulSoup(response.content,'lxml')

	totalentries = int(soup.find('totalentries').text)
	items = soup.find_all('item')

	return items

def new_search():
	user_input = input("\n\n\tEnter keywords: ").strip()

	items = call_ebay_api(keywords=user_input)

	prices = [float(item.currentprice.string) for item in items]

	if len(prices) > 0:
		high = max(prices)
		low = min(prices)
		mean = round(stats.mean(prices), 2)
		median = stats.median(prices)
		mode = stats.mode(prices)
		variance = round(stats.variance(prices, average=mean), 2)
		std_dev = round(stats.std_dev(prices, average=mean, var=variance), 2)

		print("\t" + ("_____" * 10) + "\n")
		print("\tFound " + str(len(prices)) + " different prices.")
		print("\t" + ("_____" * 10) + "\n")

		print("\tHigh:", high)
		print("\tLow:", low)
		print("\tMean:", mean)
		print("\tMedian:", median)
		print("\tMode:", mode)
		print("\tVariance:", variance)
		print("\tStandard Deviation:", std_dev)

		print("\t" + ("_____" * 10) + "\n")
		print("\tApproximately 68%% of offers are between", round(mean - std_dev, 2),"and", round(mean + std_dev, 2))
		print("\tApproximately 95%% of offers are between", round(mean - (2 * std_dev), 2),"and", round(mean + (2 * std_dev), 2))
		print("\tApproximately 99.7%% of offers are between", round(mean - (3 * std_dev), 2),"and", round(mean + (3 * std_dev), 2))
		print("\t" + ("_____" * 10) + "\n")

		print("\tAppending to Spreadsheet...")
		ss.insert_record([user_input.upper(), len(prices), high, low, mean, median, mode, variance, std_dev], ss.get_row_count() + 1 )
		print("\tFinished.")

	else:
		print("\t" + ("_____" * 10) + "\n")
		print("\tNo results were found.")
		print("\t" + ("_____" * 10) + "\n")

	print("\n")

def view_spreadsheet():
	import pprint

	pp = pprint.PrettyPrinter()

	pp.pprint(ss.get_records())

	print("\n")

def main():
	
	def main_loop():
		choice = ux.get_user_choice(OPTIONS)

		if choice == 1:
			new_search()
		elif choice == 2:
			view_spreadsheet()

	ux.to_continue(main_loop)

if __name__ == "__main__":
	main()