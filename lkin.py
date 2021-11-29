# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
import pprint
import os
import datetime
import pandas as pd
import numpy as np
import re,glob
import csv
from pandas import ExcelWriter
from time import sleep
from subprocess import PIPE, run

import json
import glob
import pandas as pd
from pandas import ExcelWriter


import sqlite3
con= sqlite3.connect('info.db')
con.execute('''CREATE TABLE IF NOT EXISTS candidate(name text,
         headline text,
         company text,
         school text,
         location text, 
         summary text,
         skills text,
         publications text,
         certifications text,
         courses text,
         projects text,
         honors text,
         languages text,
         organizations text,
         interests text,
         experiences_title text,
         experiences_company text,
         experiences_date_range text,
         experiences_location text,
         experiences_description text)''')

con.commit()
cnt=1
columns = ['url','name','role', 'employer_name']
df_ = pd.DataFrame(columns=columns)

lsst=[]

search = str(input("Enter search key: "))
chk=1
chk = int(input("page count: "))
userid = str(input("Enter email address or number with country code: "))
password = getpass.getpass('Enter your password:')

chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.linkedin.com")
driver.implicitly_wait(6)
driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()
#driver.get("https://www.linkedin.com/in/sohini-mitra-582a87129/") #Enter any of your connection profile Link
cookies_list = driver.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

li_at_id = cookies_dict.get('li_at')

search.strip()
search.replace(" ","%20")

#for i in range(1,pg+1)
pg=1

flg=True
while flg:
    lnk = "https://www.linkedin.com/search/results/people/v2/?keywords="+search+"&origin=SWITCH_SEARCH_VERTICAL&page="+str(pg)
    #driver.find_element_by_xpath("""//*[@id="ember942"]/input""").send_keys(search)
    #sleep(0.5)
    driver.get(lnk)
    pg+=1
    
    elem1 = driver.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
    driver.execute_script("window.scrollBy(0,1000)")
    #sleep(3)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight+document.body.scrollHeight);")
    elem2 = driver.find_elements_by_xpath("//a[@class='search-result__result-link ember-view']")
    elems=elem1+elem2
    
    all_elem=[]
    for elem in elems:
        if elem.get_attribute("href") not in all_elem:
            all_elem.append(elem.get_attribute("href"))
    print(all_elem)
        
    for lnk in all_elem:
        if cnt>chk:
            flg=False
            break
        cnt+=1
        try:
            driver.get(lnk)
        except:
            continue
        
        try:
            name = driver.find_element_by_xpath("//*[@class='pv-top-card-section__name inline t-24 t-black t-normal']")
            name=name.text
        except:
            name = "na"
        try:
            emp = driver.find_element_by_xpath("//*[@class='pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name text-align-left ml2 t-14 t-black t-bold lt-line-clamp lt-line-clamp--multi-line ember-view']")
            emp=emp.text
        except:
            emp= "na"
        try:
            rol = driver.find_element_by_xpath("//*[@class='pv-top-card-section__headline mt1 t-18 t-black t-normal']")
            rol=rol.text
        except:
            rol = "na"
            
        fname = "C:/data/"+name+".json"
        open(fname, 'a').close()
        #proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        #cmmd = 'scrapeli --url='+lnk+' -o "C:\Users\Simanta Sarkar\Desktop\lnk\cv\"+fname
        #cmdd ="scrapeli --url="+lnk
        #print(subprocess.Popen("scrapeli --url=", shell=True, stdout=subprocess.PIPE).stdout.read())
        #os.system("scrapeli --url=https://www.linkedin.com/in/simanta-sarkar-67991914a")
        #sleep(5)
        #print(name ,"----------------cv parsed")
        #os.system("start /wait cmd /c {scrapeli --url=https://www.linkedin.com/in/simanta-sarkar-67991914a -o 'C:\Users\Simanta Sarkar\Desktop\data.json'}")
        command = ['scrapeli', '--url='+lnk,'--li_at='+str(li_at_id), '--output_file='+fname]
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print(result.returncode, result.stdout, result.stderr)
        
        lst = [lnk,name,rol,emp]
        lsst.append(lst)
        lst = []
    
    
    
df_=pd.DataFrame(lsst,columns=['url','name','role', 'employer_name'])
 
# DF TO EXCEL
writer = ExcelWriter('PythonExport.xlsx')
df_.to_excel(writer,'Sheet5')
writer.save()

# DF TO CSV
df_.to_csv('PythonExport.csv', sep=',')


path =r'C:/data'
allFiles = glob.glob(path + "/*.json")
df = pd.DataFrame()

columns=['name','headline','company', 'school','location','summary','skills','publications','certifications','courses','projects','honors','languages','organizations','interests','experiences_title','experiences_company','experiences_date_range','experiences_location','experiences_description']
df_1 = pd.DataFrame(columns=columns)

lsst1=[]

for file_ in allFiles:

    with open(file_, "r") as read_file:
        data = json.load(read_file)
        try:
            name=data["personal_info"]["name"]
        except:
            name = ""
        try:
            headline=data["personal_info"]["headline"]
        except:
            headline=""
        try:
            company=data["personal_info"]["company"]
        except:
            company=""
        try:
            school=data["personal_info"]["school"]
        except:
            school=""
        try:
            location=data["personal_info"]["location"]
        except:
            location=""
        try:
            summary=data["personal_info"]["summary"]
        except:
            summary=""
            
        e = data['experiences']['education']
        for i in e:
            print(i["name"])
            print(i["degree"])
            print(i["grades"])
            print(i["field_of_study"])
            print(i["date_range"])
            
        e = data['experiences']['volunteering']
        for i in e:
            print(i["title"])
            print(i["company"])
            print(i["date_range"])
            print(i["location"])
            print(i["cause"])
            print(i["description"])
            
        try:
            skil = data['skills']
            skills=""
            for i in skil:
                skills+=", "+i["name"]
        except:
            skills=""
            
        try:
            pub = data['accomplishments']["publications"]
            publications=" | ".join(pub)
        except:
            publications=""
        
        try:
            cer = data['accomplishments']["certifications"]
            certifications=" | ".join(cer)
        except:
            certifications=""
            
        try:
            cou = data['accomplishments']["courses"]
            courses=" | ".join(cou)
        except:
            courses=""
        try:    
            pro = data['accomplishments']["projects"]
            projects=" | ".join(pro)
        except:
            projects=""
        
        try:
            hon = data['accomplishments']["honors"]
            honors=" | ".join(hon)
        except:
            honors=""
        try:    
            lan = data['accomplishments']["languages"]
            languages=" | ".join(lan)
        except:
            languages=""
            
        try:
            org = data['accomplishments']["organizations"]
            organizations=" | ".join(org)
        except:
            organizations=""
            
        try:
            inte = data["interests"]
            interests=" | ".join(inte)
        except:
            interests=""
        
        j = data['experiences']['jobs']
        with sqlite3.connect("info.db") as conn:
            cur = conn.cursor()
            for i in j:
                experiences_title=i["title"]
                experiences_company=i["company"]
                experiences_date_range=i["date_range"]
                experiences_location=i["location"]
                experiences_description=i["description"]
            
                cur.execute('''insert into candidate (name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description))
                con.commit()
                lst = [name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description]
                lsst1.append(lst)
                lst = []
            
df_1=pd.DataFrame(lsst1,columns=['name','headline','company', 'school','location','summary','skills','publications','certifications','courses','projects','honors','languages','organizations','interests','experiences_title','experiences_company','experiences_date_range','experiences_location','experiences_description'])
#df_1.append(df1)
            
            
# DF TO EXCEL
writer = ExcelWriter('PythonExport.xlsx')
df_1.to_excel(writer,'Sheet5')
writer.save()

# DF TO CSV
df_1.to_csv('PythonExportmrg.csv', sep=',')