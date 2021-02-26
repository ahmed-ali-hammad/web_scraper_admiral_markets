from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from config import * # logins credentials are saved in the config file
from selenium import webdriver
import time

path = "https://admiralmarkets.com/analytics/premium-analytics/dashboard?regulator=cysec"

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
options = webdriver.ChromeOptions()
driver = webdriver.Chrome("chromedriver.exe", options = options, desired_capabilities = capabilities)
driver.get(path)
time.sleep(5)

email_field = driver.find_element_by_xpath("//input[@id='field_email']")
password_field = driver.find_element_by_xpath("//input[@id='field_password']")

email_field.send_keys(Email)
password_field.send_keys(Password)
password_field.send_keys(Keys.ENTER)

time.sleep(5)

Two_Step_Verification_key = input("please enter the key from your email")

#Two_Step_Verification_field = driver.find_element_by_xpath("//input[]")
two_step_verification_field.send_keys("Two_Step_Verification_key")
two_step_verification_field.send_keys(keys.ENTER)


# logs = driver.get_log("performance")
# print(logs)
