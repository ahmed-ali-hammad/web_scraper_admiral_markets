from selenium.webdriver.common.keys import Keys
from config import * # logins credentials are saved in the config file
from seleniumwire  import webdriver
import time
import json
import csv

path = "https://admiralmarkets.com/analytics/premium-analytics/dashboard?regulator=cysec"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome("chromedriver.exe", options = options)
driver.get(path)
time.sleep(3)

email_field = driver.find_element_by_xpath("//input[@id='field_email']")
password_field = driver.find_element_by_xpath("//input[@id='field_password']")

email_field.send_keys(Email)
password_field.send_keys(Password)
password_field.send_keys(Keys.ENTER)

time.sleep(3)

Two_Step_Verification_key = input("please enter the key from your email")

two_step_verification_field = driver.find_element_by_xpath("//input[@data-cy='otp']")
two_step_verification_field.send_keys(Two_Step_Verification_key)
two_step_verification_field.send_keys(Keys.ENTER)

time.sleep(5)

driver.refresh()

time.sleep(5)


data = []
for request in driver.requests:
	if request.response:
		if "https://dashboard.acuitytrading.com/widget/GetChartPriceMacdAdmiral?" in request.url:
			network_logs_data = {
				"url":  request.url,
				"body":	json.loads(request.response.body)
	           }
			data.append(network_logs_data)

data_last_update = data[-1]['body']


simplified_data = []
for item in data_last_update:
	del item["Price"]
	del item["Bullish"]
	del item["Bearish"]
	del item["DateString"]
	simplified_data.append(item)



with open('json_data.json', 'w') as f:
	json.dump(simplified_data, f, indent = 4)

with open('csv_data.csv', 'w') as f:
	field_names = ['Macd', 'Date']
	csv_writer = csv.DictWriter(f, fieldnames= field_names)
	csv_writer.writeheader()
	for item in simplified_data:
		csv_writer.writerow(item)
	
