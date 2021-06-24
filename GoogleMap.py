from flask import Flask
from flask_restful import Api
from flask import request
from bs4 import BeautifulSoup
import requests
import validators
import re
import csv
import calendar
import time
import urllib3
from requests.exceptions import ConnectionError
from time import sleep
import numpy as np
from validate_email import validate_email


filter_type = input("enter the  search term:")
max_email_count = 0

    

def parse(phone_number):
    number = r'\d{6} \d{5}'
    phonenumber = re.finditer(number, str(phone_number))
    return(phonenumber)

def parse_email(html):
    EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.finditer(EMAIL_REGEX, str(html))
    return(emails)

def unique(email_list):
    x = np.array(email_list)
    return(np.unique(x))     

summary = []
for i in range(0,5): 
    print("page scrape: " + str(i + 1))
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    html = requests.get("https://www.google.com/search?q=" +filter_type+ "&lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:14&tbm=lcl&ei=NIPBYKyVEsLez7sP9IyAoAY&start=" + str(i*20),
                        headers=headers).text
    
    soup = BeautifulSoup(html, 'lxml')
    
    for container in soup.findAll('div', class_='VkpGBb'):
        ad = container.find('span' , class_='VqFMTc p8AiDd')
        if ad:
            continue
        heading = container.find('div', class_='dbg0pd').text
        details = container.select('span.rllt__details > div')
        article_summary = details[1 if len(details)>1 else 0 ].text

        link = container.find('a' , class_='yYlJEf L48Cpd')
        
        email_list=[]
        if(link and validators.url(link.get("href"))):
            link = link.get("href")
            try:
                x = requests.get(link).text
                emails = parse_email(x)
                for email in emails:
                    if validate_email(email.group() , check_mx=True):
                        email_list.append(email.group()) 
            except requests.ConnectionError:
                # print("OOPS!! General Error")
               email_list = ""
                
            
        
        phone_number  = parse(container.find('span', class_='rllt__details lqhpac').text)
        phone_number_list=[]
        for number in phone_number:
            phone_number_list.append(number.group()) 
        
        email_list = unique(email_list)
        
        summary_list = [heading.split('-')[0],article_summary, ", ".join(phone_number_list) , link]
        
        if max_email_count < len(email_list):
            max_email_count = len(email_list)
        
        for email in email_list:
            summary_list.append(email)
        
        summary.append(summary_list)  

fields = ['Company Name','Address','Contact Number' , 'URL' ]
for i in range(1,max_email_count):
    fields.append("Email " + str(i))
gmt = time.gmtime()
ts = str(calendar.timegm(gmt))



# writing to csv file 
with open(filter_type+'.csv','w',newline='',encoding=('utf-8')) as csvfile: 
        # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
            
    # writing the fields 
    csvwriter.writerow(fields) 
            
        # writing the data rows 
    csvwriter.writerows(summary)


