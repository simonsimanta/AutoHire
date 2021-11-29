from flask import Flask, render_template, request,Response
import sqlite3 as sql

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
import profileScraper as ps
from Company import overview

app = Flask(__name__)

import sqlite3
con= sqlite3.connect('info.db')
con.execute('''CREATE TABLE IF NOT EXISTS candidate(name text,
         phone text,
         email text,
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
         experiences_description text,
         company_name text,
         company_size text,
         company_type text,
         company_description text,
         company_industry text,
         company_location text,
         company_num_employees text,
         company_specialties text,
         company_website text,
         company_year_founded text);''')
con.execute('CREATE TABLE IF NOT EXISTS contact (name TEXT, email TEXT, phone TEXT, message TEXT)')
con.execute('CREATE TABLE IF NOT EXISTS scored (name  TEXT,company  TEXT,location  TEXT,total_org  TEXT,tenure_cur  TEXT,total_tenure  TEXT,lnk  TEXT,skill_score  TEXT,score  TEXT)')

con.commit()


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')
@app.route('/contact')
def contact():
   return render_template('contact.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():

    if request.method == 'POST':
        search = request.form['search_key']
        chk = int(request.form['num_profile'])
        userid = request.form['email']
        password = request.form['password']
        loc = request.form['Location']
        mat_skill = request.form['rq_skills']
        rq_experience = int(request.form['rq_experience'])
        rq_education = request.form['rq_education']
        
        
        rq=[rq_education,rq_experience]
        
        if loc=='Australia':
            lnkloc='facetGeoRegion=%5B"au%3A0"%5D&'
        elif loc=='Singapore':
            lnkloc='facetGeoRegion=%5B"sg%3A0"%5D&'
        elif loc=='Hyderabad':
            lnkloc='facetGeoRegion=%5B"in%3A6508"%5D&'
        elif loc=='Bengaluru':
            lnkloc='facetGeoRegion=%5B"in%3A7127"%5D&'
        elif loc=='None':
            lnkloc = ''
        
        """
        Australia=facetGeoRegion=%5B"au%3A0"%5D&
        Singapore=facetGeoRegion=%5B"sg%3A0"%5D&
        Hyderabad=facetGeoRegion=%5B"in%3A6508"%5D&
        Bengaluru=facetGeoRegion=%5B"in%3A7127"%5D&
        """
        try:
            msg = "Record successfully added"
            cnt=1
            lsst=[]
            
            columns=['name','phone','email','headline','company', 'school','location','summary','skills','publications','certifications','courses','projects','honors','languages','organizations','interests','experiences_title','experiences_company','experiences_date_range','experiences_location','experiences_description', 'company_industry', 'company_location', 'company_num_employees', 'company_specialties', 'company_website', 'company_year_founded']
            df_ = pd.DataFrame(columns=columns)
            
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
                lnk = 'https://www.linkedin.com/search/results/people/v2/?'+lnkloc+'facetNetwork=%5B"S"%5D&keywords='+search+'&origin=SWITCH_SEARCH_VERTICAL&page='+str(pg)
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
                    ut.generate(cnt,chk)
                    if cnt>chk:
                        flg=False
                        break
                    cnt+=1
                    driver.get(lnk)
                    #ps.connect(driver)
                    try:
                        driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect button-primary-large mr2 mt2']").click()
                        driver.find_element_by_xpath("//*[@class='button-secondary-large mr1']").click()
                        message="Hi, I'd like to connect."
                        driver.find_element_by_xpath("//*[@id='custom-message']").send_keys(message)
                        #driver.find_element_by_xpath("//*[@class='button-primary-large ml1']").click()
                        #sleep(5)
                    except:
                        pass
                    
                    #driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--send-in-mail button-secondary-large mr2 mt2']").click()
                    #driver.find_element_by_css_selector('.msg-overlay-bubble-header__control.js-msg-close').click()
                    
                    driver.get(lnk+'detail/contact-info/')
                    try:
                        email=driver.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-email']/div/a")
                        sleep(.1)
                        email=email.text
                        email = email.strip()
                        #ut.send_email(email)
                    except:
                        print("email not found")
                        email=""
                        
                    try:
                        phone=driver.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-phone']/ul/li/span[1]")
                        sleep(.1)
                        phone=phone.text
                    except:
                        print("phone not found")
                        phone=""
                        sleep(.1) 

                    driver.find_element_by_xpath("//*[@class='artdeco-dismiss']").click()
                    #driver.find_element_by_css_selector('.artdeco-dismiss').click()
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
                            
                            try:
                                driver.find_element_by_xpath("//span[text()='See more']").click()
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
                    
                    personal_info=ps.personal_info(soup)
                    skills = ps.skills(soup)
                    accomplishments=ps.accomplishments(soup)
                    interests = ps.interests(soup)
                    experiences = ps.experiences(soup)
                    
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
                    cur_company=company
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
                    b=0
                    m=0
                    p=0
                    b_dt=0
                    m_dt=0
                    p_dt=0
                    e = experiences['education']
                    for i in e:
                        print(i["name"])
                        print(i["degree"])
                        print(i["grades"])
                        print(i["field_of_study"])
                        print(i["date_range"])
                        if b==0:
                            b=ut.educheckB(i["degree"])
                            b_dt=ut.date_range(i["date_range"])
                        elif m==0:
                            m=ut.educheckM(i["degree"])
                            if m==1:
                                m_dt=ut.date_range(i["date_range"])
                        elif p==0:
                            p=ut.educheckP(i["degree"])
                            if p==1:
                                p_dt=ut.date_range(i["date_range"])
                        
                    '''e = experiences['volunteering']
                    for i in e:
                        print(i["title"])
                        print(i["company"])
                        print(i["date_range"])
                        print(i["location"])
                        print(i["cause"])
                        print(i["description"])'''
                        
                    try:
                        skil = skills
                        skills=""
                        for i in skil:
                            skills+=","+i["name"]
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
                        
                    #company
                    
                    a=soup.find("a", attrs={"data-control-name":'background_details_company'})
                    cmp="https://www.linkedin.com"+a['href']
                    #cmp=company
                    #cmp=cmp.lower()
                    #cmp=cmp.strip()
                    #cmp = cmp.replace(' ','-')
                    #company_lnk = "https://www.linkedin.com/company/"+cmp+"/"
                    
                    try:
                        driver.get(cmp)
                    
                        html1 = driver.page_source
                        overview_soup= BeautifulSoup(html1,"html.parser")
                        cmp_ovr = overview(overview_soup)
                    
                        company_size = str(cmp_ovr['company_size'])
                        company_type = str(cmp_ovr['company_type'])
                        company_description = str(cmp_ovr['description'])
                        company_industry = str(cmp_ovr['industry'])
                        company_location = str(cmp_ovr['location'])
                        company_name = str(cmp_ovr['name'])
                        company_num_employees = str(cmp_ovr['num_employees'])
                        comp_specialties = cmp_ovr['specialties']
                        company_specialties =str("".join(comp_specialties))
                        company_website = str(cmp_ovr['website'])
                        company_year_founded = str(cmp_ovr['year_founded'])
                    except Exception as e:
                        print(e)
                        company_size = ""
                        company_type = ""
                        company_description = ""
                        company_industry = ""
                        company_location = ""
                        company_name = ""
                        company_num_employees = ""
                        comp_specialties = ""
                        company_specialties = ""
                        company_website = ""
                        company_year_founded = ""
                        
                    j = experiences['jobs']
                    with sqlite3.connect("info.db") as con:
                        cur = con.cursor()
                        #work_key = len(j)
                        
                        pos=[]
                        pos_count=0
                        tenure=[]
                        cmp_cnt=[]
                        if len(j)!=0:
                            total_it_pro=1
                            lst_cmp=''
                            tenure_cur=0
                            for i in j:
                                experiences_title=i["title"]
                                if i["title"] not in pos:
                                    pos.append(i["title"])
                                    pos_count+=1
                                experiences_company=i["company"]
                                
                                if i["company"] not in cmp_cnt:
                                    cmp_cnt.append(i["company"])
                                experiences_date_range=i["date_range"]
                                #experiences_date_range=i["total_tenure"]
                                if cur_company == i["company"]:
                                    tenure_cur = ut.tenure(i['total_tenure'])
                                experiences_location=i["location"]
                                experiences_description=i["description"]
                                tenure.append(ut.tenure(i['total_tenure']))
                                if lst_cmp==i["company"]:
                                    total_it_pro+=1
                                else:
                                    lst_cmp=i["company"]
                                
                                print(experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description)
                                cur.execute('''insert into candidate(name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded) 
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded,))
                                #con.commit()
                                lst = [name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded]
                                lsst.append(lst)
                                lst = []
                                
                            total_tenure = sum(tenure)
                            within_pro_avg = (total_tenure)/pos_count
                            org_cng_avg = (total_tenure)/len(cmp_cnt)
                            total_org=len(cmp_cnt)
                            if len(cmp_cnt) !=0:
                                event = 1
                            else:
                                event = 0
                            
                            skill_score=ut.skill_match(mat_skill,skills)
                            print("++++++++++++++++++++++++++++")
                            da=[total_org,tenure_cur,total_tenure,within_pro_avg,total_it_pro,org_cng_avg,event,b,m,p,b_dt,m_dt,p_dt,skill_score]
                            score=ut.score_cal(rq,da) 
                            print(name,company,location,lnk,total_org,tenure_cur,total_tenure,within_pro_avg,total_it_pro,org_cng_avg,event,b,m,p,b_dt,m_dt,p_dt,skill_score)
                            print("++++++++++++++++++++++++++++")
                            print(score)
                            
                            cur.execute('''insert into scored(name,company,location,total_org,tenure_cur,total_tenure,lnk,skill_score,score) 
                                    VALUES(?,?,?,?,?,?,?,?,?)''', (name,company,location,total_org,tenure_cur,total_tenure,lnk,skill_score,score))
                        else:
                            experiences_title=""
                            experiences_company=""
                            experiences_date_range=""
                            experiences_location=""
                            experiences_description=""
                    
                            cur.execute('''insert into candidate(name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded) 
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded))
                            
                            lst = [name,phone,email,headline,company, school,location,summary,skills,publications,certifications,courses,projects,honors,languages,organizations,interests,experiences_title,experiences_company,experiences_date_range,experiences_location,experiences_description,company_name, company_size, company_type, company_description, company_industry, company_location, company_num_employees, company_specialties, company_website, company_year_founded]
                            lsst.append(lst)
                            lst = []
                            
                        con.commit()
                            #print(name,headline,company,school,location,summary,email)
                            #pprint.pprint(skills, width=1)
                            #pprint.pprint(interests, width=1)
                            #pprint.pprint(experiences, width=1)
        except Exception as e:
            con.rollback()
            msg = e
        finally:
            df_=pd.DataFrame(lsst,columns=['name','phone','email','headline','company', 'school','location','summary','skills','publications','certifications','courses','projects','honors','languages','organizations','interests','experiences_title','experiences_company','experiences_date_range','experiences_location','experiences_description','company_name', 'company_size', 'company_type', 'company_description', 'company_industry', 'company_location', 'company_num_employees', 'company_specialties', 'company_website', 'company_year_founded'])
            #df_1.append(df1)
                        
                        
            # DF TO EXCEL
            writer = ExcelWriter('PythonExport.xlsx')
            df_.to_excel(writer,'Sheet5')
            writer.save()        
            driver.quit()
            #return Response(generate(), mimetype= 'text/event-stream')
            return render_template("result.html",msg = msg)
            con.close()
                    
@app.route('/contactus',methods = ['POST', 'GET'])
def contactus():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         phone = request.form['phone']
         message = request.form['message']
         
         with sql.connect("info.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO contact (name,email,phone,message) VALUES (?,?,?,?)",(name,email,phone,message) )
            
            con.commit()
            msg = "Record successfully added"
      except Exception as e:
          con.rollback()
          msg = e
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("info.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from candidate")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/contactinfo')
def contactinfo():
   con = sql.connect("info.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from contact")
   
   rows = cur.fetchall();
   return render_template("contactinfo.html",rows = rows)

@app.route('/scored')
def scored():
   con = sql.connect("info.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from scored order by score desc")
   
   rows = cur.fetchall();
   return render_template("scored.html",rows = rows)

if __name__ == '__main__':
   app.run(host='0.0.0.0')#host='0.0.0.0',debug=True