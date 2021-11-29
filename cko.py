# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 11:45:10 2018

@author: SimantaSarkar
"""

import time
from selenium import webdriver

userid = str(input("Enter email address or number with country code: "))
password = str(input('Enter your password:'))

chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
driver.implicitly_wait(6)
driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()
#time.sleep(2)

cookies_list = driver.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

session_id = cookies_dict.get('li_at')
print(session_id)

driver.quit()