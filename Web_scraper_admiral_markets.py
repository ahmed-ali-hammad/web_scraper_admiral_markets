from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from config import * # logins credentials are stored in the config file
import pandas as pd
import json
import time
import csv

currency_pairs = ['EURJPY', 'EURAUD', 'AUDUSD', 'EURCHF', 'USDJPY', 'EURCAD', 'NZDUSD', 'GBPJPY', 'EURUSD', 'GBPUSD', 'USDCHF', 'USDCAD', 'AUDNZD']
path = "https://admiralmarkets.com/analytics/premium-analytics/dashboard?regulator=cysec"

options = webdriver.ChromeOptions()
# options.add_argument("--incognito")
driver = webdriver.Chrome("chromedriver.exe", options = options)
driver.get(path)
time.sleep(2) # to make sure the page is entirely loaded before locating the elements

# loging in to the site
email_field = driver.find_element_by_xpath("//input[@id='field_email']")
password_field = driver.find_element_by_xpath("//input[@id='field_password']")
email_field.send_keys(Email)
password_field.send_keys(Password)
password_field.send_keys(Keys.ENTER)

time.sleep(3) # to make sure the page is entirely loaded before locating the elements

Two_Step_Verification_key = input("please enter the key from your email")
two_step_verification_field = driver.find_element_by_xpath("//input[@data-cy='otp']")
two_step_verification_field.send_keys(Two_Step_Verification_key)
two_step_verification_field.send_keys(Keys.ENTER)

time.sleep(5)

driver.refresh()

time.sleep(5)

class AdmiralMarketsScraper: # scraper class
	def __init__(self, currency_pair):
		self.currency_pair = currency_pair
		self.data = []
		self.simplified_data = []

	def collect_data(self): # responsible for excuting all the other methods inside the class
		self.start_search()
		data_last_update = self.get_data()
		simplified_data = self.simplify_data(data_last_update)
		self.save_data()

	def start_search(self): # responsibel for starting the search for the given currency pair
		search_field = driver.find_element_by_xpath("//input[@placeholder='Search instrument']")
		search_field.send_keys(Keys.CONTROL + "a")
		search_field.send_keys(Keys.DELETE)
		search_field.send_keys(self.currency_pair)
		search_field.send_keys(Keys.ENTER)
		search_container = driver.find_element_by_xpath("//div[@class='instrument ng-star-inserted']")
		search_button = search_container.find_element_by_tag_name('a')
		time.sleep(3) # waiting for the data to load
		search_button.click() 

	def get_data(self): # responsible for collecting the data from the network traffic
		for request in driver.requests:
			if request.response:
				if "https://dashboard.acuitytrading.com/widget/GetChartPriceMacdAdmiral?" in request.url:
					network_logs_data = {
						"url":  request.url,
						"body":	json.loads(request.response.body)
			           }
					self.data.append(network_logs_data)
		data_last_update = self.data[-1]['body']
		return data_last_update

	def simplify_data(self, data_last_update):
		for item in data_last_update:
			del item["Price"]
			del item["Bullish"]
			del item["Bearish"]
			del item["DateString"]
			self.simplified_data.append(item)
		return self.simplified_data

	def save_data(self): # responsible for saving the data to the csv file
		try:
			with open(f'{self.currency_pair} MACD & DATE.csv', 'a') as f:
				field_names = ['Macd', 'Date']
				csv_writer = csv.DictWriter(f, fieldnames = field_names)
				for item in self.simplified_data:
					csv_writer.writerow(item)
		except FileNotFoundError:
			with open(f'{self.currency_pair} MACD & DATE.csv', 'w') as f:
				field_names = ['Macd', 'Date']
				csv_writer = csv.DictWriter(f, fieldnames = field_names)
				csv_writer.writeheader()
				for item in self.simplified_data:
					csv_writer.writerow(item)

		# removing the duplicates
		with open(f'{self.currency_pair} MACD & DATE.csv', 'r+') as f:
			table = pd.read_csv(f'{self.currency_pair} MACD & DATE.csv')
			clean_table = table.drop_duplicates()
			f.seek(0)
			clean_table.to_csv(f'{self.currency_pair} MACD & DATE.csv', index=False)


if __name__ == '__main__':
	for currency in currency_pairs:
		currency_pair = AdmiralMarketsScraper(currency)
		currency_pair.collect_data()
	print('Data was updated')
