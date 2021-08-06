""" Scraping Canadian Charity Website with Selenium """
import os
import json 
import requests
import selenium
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
DRIVER_PATH = '/usr/local/bin/chromedriver'
import base64
import time
import urllib.request
from pprint import pprint
import pandas as pd
from selenium.common import exceptions

SAVE_FOLDER = ''

# set up driver 
driver = webdriver.Chrome(DRIVER_PATH)
# set up link 
BASE_LINK = "https://www.yelp.ca/search?find_desc=Black%20Owned%20Businesses&find_loc=Toronto%2C%20ON&start=";

# start page is 0
start = 0
# create dataframe to hold businesses 
columns = ['business_name', 'business_website_url', 'business_phone_no', 'business_address', 'cause1', 'business_description']
bl_businesses = pd.DataFrame(columns = columns)

for i in range(1,24): 
    LINK = BASE_LINK + str(start) 
       
    count = 0
    
    while count < 10:
        try: 
            driver.get(LINK)
            # time.sleep(1)
            print('count: '+ str(count))
            # get the black owned businesses
            business = driver.find_elements_by_class_name('css-166la90')[count]
            # pprint(business.find_element_by_class_name('css-8jxw1i'))

            # get business name 
            if(business.get_attribute('innerHTML') is not None): 
                business_name =  business.get_attribute('innerHTML')
            else: 
                business_name = ""

            # after getting the business name we go into the url 
            business_href = business.get_attribute('href')
            # then we go into the href 
            driver.get(business_href)

            # get business website url 
            if(len(driver.find_elements_by_css_selector('p.css-1h1j0y3>a.css-ac8spe')) > 0): 
                business_website_url = driver.find_element_by_css_selector('p.css-1h1j0y3>a.css-ac8spe').get_attribute('innerHTML')
            else: 
                business_website_url = " "

            # next we get the phone number
            if(len(driver.find_elements_by_css_selector('div>p.css-1h1j0y3'))> 2): 
                print('length ' + str(len(driver.find_elements_by_css_selector('div>p.css-1h1j0y3'))))
                business_phone_no = driver.find_elements_by_css_selector('div>p.css-1h1j0y3')[2].get_attribute('innerHTML')
                # business_phone_no = " " 
            else: 
                business_phone_no = " "
            
            # some times it's the first index and not the second one
            if('<a href=' in business_phone_no and len(driver.find_elements_by_css_selector('div>p.css-1h1j0y3')) > 1): 
                business_phone_no = driver.find_elements_by_css_selector('div>p.css-1h1j0y3')[1].get_attribute('innerHTML')


            business_address = " "
            # next we get their address
            if(len(driver.find_elements_by_css_selector('span.raw__373c0__14n8z')) > 0):
                address_info = driver.find_elements_by_css_selector('span.raw__373c0__14n8z')
                for addy in address_info: 
                    business_address += " " + addy.get_attribute('innerHTML')

            # we also need to get the business description 
            business_description = " "; 
            if(len(driver.find_elements_by_class_name('css-gdi06s')) > 1):
                print("I think this is the out of range")
                if("so businesses can't pay to alter or remove their" in driver.find_elements_by_class_name('css-gdi06s')[1].get_attribute("innerHTML")):
                    business_description = driver.find_elements_by_class_name('css-gdi06s')[0].get_attribute("innerHTML")
                else:
                    business_description = driver.find_elements_by_class_name('css-gdi06s')[1].get_attribute("innerHTML")

            # clean business description a little bit
            business_description  = business_description.replace("<span>"," ")\
                                .replace("</span>", " ")\
                                .replace("<div>", " ")\
                                .replace("</div>", " ")\
                                .replace("<span", " ")\
                                .replace("width= ", " ")\
                                .replace("0", " ")
            print(business_description)
            bl_businesses = bl_businesses.append({
                'business_name': business_name, 
                'business_website_url': business_website_url, 
                'business_phone_no': business_phone_no, 
                'business_address': business_address, 
                'business_description': business_description,
                'cause1': 'black owned businesses'
            }, ignore_index=True)

            pprint(bl_businesses)

        except IndexError as e: 
            print(e)
        except exceptions.NoSuchElementException as e: 
            print(e)
        except exceptions.WebDriverException as e: 
            print(e)
        finally: 
            count += 1
    start += 10

driver.close()
        

bl_businesses.to_csv('black_owned_businesses_in_toronto_2.csv')
