# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 11:14:57 2018

@author: SimantaSarkar
"""

import smtplib
#from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
 #email.mime.text.MIMEText
 
fromaddr = ""  #from email 
toaddr = ""    #to email
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test mail" 
 
body = "hi,test mail"
msg.attach(MIMEText(body, 'plain'))
 
#select smtp server
#server = smtplib.SMTP('smtp.gmail.com', 587)
server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
#server = smtplib.SMTP(host='smtp.mail.yahoo.com', port=587)

server.starttls()
server.login(fromaddr, "password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()