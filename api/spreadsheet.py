import gspread
from oauth2client.service_account import ServiceAccountCredentials

'''
	A script to encapsulate Google Sheets API. The specific spreadsheet is hardcoded.
'''

SCOPE = ['https://spreadsheets.google.com/feeds']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('../client_secret.json', SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open('Ebay Scrape Samples').sheet1

# Wrappers
insert_record = SHEET.insert_row
get_records = SHEET.get_all_records

def get_row_count():
	return SHEET.row_count

def main():
	
	print("\n")

	records = SHEET.get_all_records()
	a = "Testing the insertion method".split()

	insert_record(a, SHEET.row_count + 1)
	records = get_records()

	print("\n")


if __name__ == "__main__":
	main()