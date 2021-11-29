# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 11:52:21 2018

@author: SimantaSarkar
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
import utils as ut
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

def personal_info(soup):
    """Return dict of personal info about the user"""
    top_card = ut.one_or_default(soup, 'section.pv-top-card-section')

    personal_info = ut.get_info(top_card, {
        'name': 'h1.pv-top-card-section__name',
        'headline': '.pv-top-card-section__headline',
        'company': '.pv-top-card-v2-section__company-name',
        'school': '.pv-top-card-v2-section__school-name',
        'location': '.pv-top-card-section__location',
        'summary': 'p.pv-top-card-section__summary-text'
    })
    followers_text = ut.text_or_default(soup,
                                     '.pv-recent-activity-section__follower-count-text', '')
    personal_info['followers'] = followers_text.replace(
        'followers', '').strip()
    return personal_info

def interests(soup):
    """
    Returns:
        list of person's interests
    """
    container = ut.one_or_default(soup, '.pv-interests-section')
    interests = ut.all_or_default(container, 'ul > li')
    interests = map(lambda i: ut.text_or_default(
        i, '.pv-entity__summary-title'), interests)
    return list(interests)

def accomplishments(soup):
    """
    Returns:
        dict of professional accomplishments including:
            - publications
            - cerfifications
            - patents
            - courses
            - projects
            - honors
            - test scores
            - languages
            - organizations
    """
    accomplishments = dict.fromkeys([
        'publications', 'certifications', 'patents',
        'courses', 'projects', 'honors',
        'test_scores', 'languages', 'organizations'
    ])
    container = ut.one_or_default(soup, '.pv-accomplishments-section')
    for key in accomplishments:
        accs = ut.all_or_default(container, 'section.' + key + ' ul > li')
        accs = map(lambda acc: acc.get_text() if acc else None, accs)
        accomplishments[key] = list(accs)
    return accomplishments
    
    
def skills(soup):
    """
    Returns:
        list of skills {name: str, endorsements: int} in decreasing order of
        endorsement quantity.
    """
    skills = soup.select('.pv-skill-category-entity__skill-wrapper')
    skills = list(map(ut.get_skill_info, skills))

    # Sort skills based on endorsements.  If the person has no endorsements
    def sort_skills(x): return int(
        x['endorsements'].replace('+', '')) if x['endorsements'] else 0
    return sorted(skills, key=sort_skills, reverse=True)

def experiences(soup):
    """
    Returns:
        dict of person's professional experiences.  These include:
            - Jobs
            - Education
            - Volunteer Experiences
    """
    experiences = {}
    container = ut.one_or_default(soup, '.background-section')

    jobs = ut.all_or_default(
        container, '#experience-section ul .pv-position-entity')
    jobs = list(map(ut.get_job_info, jobs))
    jobs = ut.flatten_list(jobs)
    experiences['jobs'] = jobs

    schools = ut.all_or_default(
        container, '#education-section .pv-education-entity')
    schools = list(map(ut.get_school_info, schools))
    experiences['education'] = schools

    volunteering = ut.all_or_default(
        container, '.pv-profile-section.volunteering-section .pv-volunteering-entity')
    volunteering = list(map(ut.get_volunteer_info, volunteering))
    experiences['volunteering'] = volunteering

    return experiences

cnt=1
lsst=[]

columns=['name','headline','company', 'school','location','summary','skills','publications','certifications','courses','projects','honors','languages','organizations','interests','experiences_title','experiences_company','experiences_date_range','experiences_location','experiences_description']
df_ = pd.DataFrame(columns=columns)

search = "angularjs" #str(input("Enter search key: "))
chk = 1#int(input("page count: "))
userid = "rhea_bonnerji@yahoo.com"#str(input("Enter email address or number with country code: "))
password = "bayshore179"#getpass.getpass('Enter your password:')

chrome_path = './chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.set_window_size(1366, 768)
driver.get("https://www.linkedin.com")
driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()

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
    sleep(3)
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
        driver.get(lnk+'detail/contact-info/')
        try:
            email=driver.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-email']/div/a")
            sleep(1)
            email=email.text
        except:
            email=""
            sleep(.1)
        try:
            phone=driver.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-phone']/ui/li/span[1]")
            sleep(1)
            phone=email.text
        except:
            phone=""
            sleep(.1)    
        driver.find_element_by_css_selector('.artdeco-dismiss').click()    
        #scroll
        expandable_button_selectors = [
            'button[aria-expanded="false"].pv-skills-section__additional-skills',
            'button[aria-expanded="false"].pv-profile-section__see-more-inline',
            'button[aria-expanded="false"].pv-top-card-section__summary-toggle-button',
            'button[data-control-name="contact_see_more"]'
        ]
        
        scroll_increment=300
        scroll_pause=0.1
        current_height = 0
        while True:
            for name in expandable_button_selectors:
                try:
                    driver.find_element_by_css_selector(name).click()
                except:
                    pass
            # Scroll down to bottom
            new_height = driver.execute_script(
                "return Math.min({}, document.body.scrollHeight)".format(current_height + scroll_increment))
            if (new_height == current_height):
                break
            driver.execute_script(
                "window.scrollTo(0, Math.min({}, document.body.scrollHeight));".format(new_height))
            current_height = new_height
            # Wait to load page
            sleep(scroll_pause)
        
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        
        personal_info=personal_info(soup)
        skills = skills(soup)
        accomplishments=accomplishments(soup)
        interests = interests(soup)
        experiences = experiences(soup)
        
        try:
            name= personal_info["name"]
        except:
            name = ""
        try:
            headline=personal_info["headline"]
        except:
            headline=""
        try:
            company=personal_info["company"]
        except:
            company=""
        try:
            school=personal_info["school"]
        except:
            school=""
        try:
            location=personal_info["location"]
        except:
            location=""
        try:
            summary=personal_info["summary"]
        except:
            summary=""
            
        e = experiences['education']
        for i in e:
            print(i["name"])
            print(i["degree"])
            print(i["grades"])
            print(i["field_of_study"])
            print(i["date_range"])
            
        e = experiences['volunteering']
        for i in e:
            print(i["title"])
            print(i["company"])
            print(i["date_range"])
            print(i["location"])
            print(i["cause"])
            print(i["description"])
            
        try:
            skil = skills
            skills=""
            for i in skil:
                skills+=", "+i["name"]
        except:
            skills=""
            
        try:
            pub = accomplishments["publications"]
            publications=" | ".join(pub)
        except:
            publications=""
        
        try:
            cer = accomplishments["certifications"]
            certifications=" | ".join(cer)
        except:
            certifications=""
            
        try:
            cou = accomplishments["courses"]
            courses=" | ".join(cou)
        except:
            courses=""
        try:    
            pro = accomplishments["projects"]
            projects=" | ".join(pro)
        except:
            projects=""
        
        try:
            hon = accomplishments["honors"]
            honors=" | ".join(hon)
        except:
            honors=""
        try:    
            lan = accomplishments["languages"]
            languages=" | ".join(lan)
        except:
            languages=""
            
        try:
            org = accomplishments["organizations"]
            organizations=" | ".join(org)
        except:
            organizations=""
            
        try:
            inte = interests
            interests=" | ".join(inte)
        except:
            interests=""
        
        j = experiences['jobs']
        
        if len(j)!=0:
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
                    conn.commit()
                    lst = [name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description]
                    lsst.append(lst)
                    lst = []
        else:
            experiences_title=""
            experiences_company=""
            experiences_date_range=""
            experiences_location=""
            experiences_description=""
        
            cur.execute('''insert into candidate (name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description))
            conn.commit()
            lst = [name,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description]
            lsst.append(lst)
            lst = []
        
        #print(name,headline,company,school,location,summary,email)
        pprint.pprint(skills, width=1)
        pprint.pprint(interests, width=1)
        pprint.pprint(experiences, width=1)
        
df_=pd.DataFrame(lsst,columns=['name','headline','company', 'school','location','summary','skills','publications','certifications','courses','projects','honors','languages','organizations','interests','experiences_title','experiences_company','experiences_date_range','experiences_location','experiences_description'])
#df_1.append(df1)
            
            
# DF TO EXCEL
writer = ExcelWriter('PythonExport.xlsx')
df_.to_excel(writer,'Sheet5')
writer.save()        
driver.quit()