from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup

import statistics as stats

# API
APP_ID = "GabrielF-Scraper-PRD-4134e8f72-f88173a5"

def call_api(keywords=None):

	api = finding(appid=APP_ID, config_file=None)
	api_request = { 'keywords': keywords }
	response = api.execute('findItemsByKeywords', api_request)
	soup = BeautifulSoup(response.content,'lxml')

	totalentries = int(soup.find('totalentries').text)
	items = soup.find_all('item')

	return items
	
def main():

	user_input = input("\n\n\tEnter a search: ")

	items = call_api(keywords=user_input)

	prices = []

	for item in items:
		# category = item.categoryname.string.upper()
		# title = item.title.string.upper()
		prices.append(round(float(item.currentprice.string), 2))
		# url = item.viewitemurl.string

	if len(prices) > 0:
		prices.sort()
		high = prices[len(prices) - 1]
		low = prices[0]
		mean = round(stats.mean(prices), 2)
		median = stats.median(prices)
		mode = stats.mode(prices)
		variance = round(stats.variance(prices, average=mean), 2)
		std_dev = round(stats.std_dev(prices, average=mean, var=variance), 2)

		print("\t" + ("_____" * 10) + "\n")
		print("\t\tHigh", high)
		print("\t\tLow", low)
		print("\t\tMean:", mean)
		print("\t\tMedian:", median)
		print("\t\tMode:", mode)
		print("\t\tVariance:", variance)
		print("\t\tStandard Deviation:", std_dev)
		print("\t" + ("_____" * 10) + "\n")

		print("\tApproximately 68%% of offers are between", round(mean - std_dev, 2),"and", round(mean + std_dev, 2))
		print("\tApproximately 95%% of offers are between", round(mean - (2 * std_dev), 2),"and", round(mean + (2 * std_dev), 2))
		print("\tApproximately 99.7%% of offers are between", round(mean - (3 * std_dev), 2),"and", round(mean + (3 * std_dev), 2))
		print("\t" + ("_____" * 10) + "\n")
	else:
		print("\t" + ("_____" * 10) + "\n")
		print("\tNo results were found.")
		print("\t" + ("_____" * 10) + "\n")

	print("\n\n")

if __name__ == "__main__":
	main()