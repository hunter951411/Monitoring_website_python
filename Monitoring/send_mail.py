import smtplib
import imaplib
import email
import os
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
import mimetypes

def send_mail(timedie,mailreport):
	server = smtplib.SMTP()
	EMAIL_ACCOUNT = "Bcct28042016@gmail.com"
	EMAIL_PASS = "HelloVietNam28042016"
	server.connect('smtp.gmail.com', port = 587) 
	server.ehlo()
	server.starttls()
	server.login(EMAIL_ACCOUNT, EMAIL_PASS)
	fromaddr = "VNIST Report"
	msg = email.MIMEMultipart.MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = email.Utils.COMMASPACE.join(mailreport.split())
	msg['Subject'] = "Website Status" 
	msg.attach(MIMEText("Website die in "+ str(timedie)))
	msg.attach(MIMEText('nsent via python', 'plain')) 
	server.sendmail(EMAIL_ACCOUNT,mailreport.split(),msg.as_string())
