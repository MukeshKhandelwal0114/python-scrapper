# from flask import Flask
# from flask_restful import Resource, Api

# app = Flask(__name__)
# api = Api(app)

# @app.route('/', methods=['GET'])
# def home():
from selenium import webdriver
import base64
import requests
import urllib.parse as urlparse
import time
from selenium.webdriver.support.ui import Select
from PIL import Image
from selenium.webdriver.chrome.options import Options
import csv
import calendar
import time
import urllib3
from requests.exceptions import ConnectionError
from time import sleep
import numpy as np
from validate_email import validate_email

def contact_info(number):
    mapping = {
        "mobilesv icon-ba": '-',
        "mobilesv icon-acb": '0',
        "mobilesv icon-yz": '1',
        "mobilesv icon-wx": '2',
        "mobilesv icon-vu": '3',
        "mobilesv icon-ts": '4',
        "mobilesv icon-rq": '5',
        "mobilesv icon-po": '6',
        "mobilesv icon-nm": '7',
        "mobilesv icon-lk": '8',
        "mobilesv icon-ji": '9',
    }
    if number in mapping:
        return mapping[number]
    else:
        return ''
    
filter_type = input("enter the search term: ") or 'Sweet Shop'

city = input("enter the city: ") or 'Jaipur'

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe", options=options)

# to maximize the browser window
driver.maximize_window()
#get method to launch the URL
summary =[]
driver.get("https://www.justdial.com/" + city + "/search?q=" +filter_type)

# driver.get("https://www.justdial.com/" + city + "/" +filter_type + "/page=1")
# url = driver.current_url
# print(url)
a = driver.find_elements_by_class_name('//*[@id="morehvr_add_cont1"]/span[2]')
print(a)
list_of_hrefs = []



content_blocks = driver.find_elements_by_class_name("jpag")

for block in content_blocks:
    elements = block.find_elements_by_tag_name("a")
    for el in elements:
        list_of_hrefs.append(el.get_attribute("href"))
        

for i in range(0, 3):
    driver.delete_all_cookies()
    driver.get(list_of_hrefs[1].replace('-2', '-' + str(i+1)))        
    detail = driver.find_elements_by_class_name("cntanr")
    if len(detail) == 0:
        break
    for container in detail:
        title = container.find_element_by_class_name("jcn").text        
        # print(title)      
        # print(container.text)
        contact_info_list = container.find_elements_by_class_name('mobilesv')
        phone_number = ''
        for phone in contact_info_list:
            phone_number += contact_info(phone.get_attribute('class'))  
              
        # print(phone_number)
        # print(contact_info)
        # print(title)
        summary_list = [title , phone_number]
        summary.append(summary_list)        
    print("page scrape: " + str(i + 1))    
              
    fields = ['title','Contact Number' ]
    with open(filter_type+'.csv','w',newline='',encoding=('utf-8')) as csvfile:
        
        csvwriter = csv.writer(csvfile) 
                
        # writing the fields 
        csvwriter.writerow(fields) 
                
            # writing the data rows 
        csvwriter.writerows(summary)
        
driver.close()