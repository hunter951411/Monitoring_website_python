import socket
import subprocess
import re
import datetime
import httplib
from selenium import webdriver
from PIL import Image
import mysql.connector
from threading import Thread
import time
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

server = smtplib.SMTP()
EMAIL_ACCOUNT = "Bcct28042016@gmail.com"
EMAIL_PASS = "HelloVietNam28042016"
server.connect('smtp.gmail.com', port = 587) 
server.ehlo()
server.starttls()
server.login(EMAIL_ACCOUNT, EMAIL_PASS)

conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
                        password='trung',database='demo1')

c = conn.cursor()
mang = []
#url = raw_input("Url:")
print "Start: "+str(datetime.datetime.now())
#nhan thong tin ping
def ping_time(url):
	ping = subprocess.Popen(["ping", "-c", "1", url],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	i = datetime.datetime.now()
	s = i.strftime('%Y-%m-%d %H:%M:%S')
	#print "Time current: %s"%s
	out, error = ping.communicate()
	regexIp = "\s?\((.+?)\)\s?"
	Ip = re.findall(regexIp, out)
	#print "Ip="+Ip[0]
	regexTime ="\s?time=(.+?)\s?ms"
	Time = re.findall(regexTime,out)
	regexReceive = "\s?transmitted,\s?(.+?)\s?received"
	ReceiveResult = re.findall(regexReceive, out)
	if (len(ReceiveResult)==0):
		print "No Network Connection!!!"
		Timeresult= 0
	else:
		if int(ReceiveResult[0])== 0:
			print "ping failed"
			Timeresult= 0	
		elif int(ReceiveResult[0])== 1:
			Timeresult= Time[0]
	return Timeresult

#nhan thong tin get
def get_time(url):
	startget = datetime.datetime.now()	
	#print startget
	try:
		conn = httplib.HTTPConnection(url)
		conn.request("GET", "/")
		r1 = conn.getresponse()
		endget = datetime.datetime.now()
		gettimeinsert = (endget-startget)
		#print endget
		#print r1.status, r1.reason
		intr1status = (int(r1.status))/100
	except:
		intr1status =0
	#if (intr1status == 0):
	#	print "Loi"
	#elif (intr1status == 1):
	#	print "1xx"
	#elif (intr1status == 2):
	#	print "2xx"
	#elif (intr1status == 3):
	#	print "3xx"
	if (intr1status == 5 or intr1status == 4):
		status = 1
		conn.commit()	
		find ="Select MailReport from updatetable where Url='"+url+"'"
		c.execute(find)
		for row in c:
			#print (row[0])		
			SendMail(startget,row[0])	
	elif(intr1status == 0):
		status = 2
		conn.commit()
		find ="Select MailReport from updatetable where Url='"+url+"'"
		c.execute(find)
		for row in c:
			#print (row[0])		
			SendMail(startget,row[0])
	else:
		status = 0
	conn.close()
	timeget = float(gettimeinsert.total_seconds() * 1000)
	timeget = timeget * 100
	timeget = int(timeget)
	timeget = float(timeget)/100
	#print float(timeget)
	return float(timeget),status


#chup anh website
def screenshot(url,s):
	browser = webdriver.Firefox()
	urlfull = "http://"+url+"/"
	#print urlfull
	browser.get(urlfull)
	name = "Pictures/"+url+".png"
	#print name
	browser.save_screenshot(name)
	browser.quit()
	img = Image.open(name)
	img1 = img.crop((0, 0, 1000, 800))
	img1.save(name)
	return name

def process_update(s):
	print "mang update"
	print mang
	del mang[:]
	print mang
	conn.commit()	
	find ="Select Url from updatetable"
	c.execute(find)
	for row in c:
		#print (row[0])		
		mang.append(row[0])

	for x in mang:
		#screenshot(x)
		if (run_update(x,s)==2):
			break
		
		else:
			Thread(target=screenshot, args=(x,s)).start()
			time.sleep(2)
		#print x
	#time.sleep(40)

        for x in mang:
		#print x
		Thread(target=run_update, args=(x,s,)).start()
		time.sleep(1)

def process_insert(s):
	print "Mang insert"
	print mang
	del mang[:]
	print mang
	#conn.commit()	
	find ="Select Url from updatetable"
	c.execute(find)
	for row in c:
		#print (row[0])		
		mang.append(row[0])

	for x in mang:
		#print x
		Thread(target=run_insert, args=(x,s,)).start()
		time.sleep(1)

def get_ip(url):
	return socket.gethostbyname(url)

def run_update(url,s):
	#conn.commit()
	Active = get_time(url)[1]	
	update ="Update updatetable set Ip='"+str(get_ip(url))+"', LastPingTime='"+str(ping_time(url))+"', LastGetTime='"+str(get_time(url)[0])+"', Picture='"+"Pictures/"+url+".png"+"',LastTime='"+str(s)+"',Active='"+str(Active)+"' Where Url='"+url+"'"
	print update
	c.execute(update,multi = True)
	conn.commit()
	return	Active 	

def run_insert(url,s):
	#conn.commit()
	Active = get_time(url)[1]
	insert ="Insert into inserttable(Url,PingTime,GetTime,Active,Time) Values('"+str(url)+"', '"+str(ping_time(url))+"', '"+str(get_time(url)[0])+"',"+str(Active)+",'"+str(s)+"')"
	print insert
	c.execute(insert,multi = True)
	conn.commit()	
	
def SendMail(timedie,mailreport):
	fromaddr = "VNIST Report"
	msg = email.MIMEMultipart.MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = email.Utils.COMMASPACE.join(mailreport.split())
	msg['Subject'] = "Website Status" 
	msg.attach(MIMEText("Website die in "+ str(timedie)))
	msg.attach(MIMEText('nsent via python', 'plain')) 
	server.sendmail(EMAIL_ACCOUNT,mailreport.split(),msg.as_string())

mang1 = []
def checktime():
	i = datetime.datetime.now()
	u = int(i.strftime('%M'))
	s = i.strftime('%Y-%m-%d %H:%M:%S')
	#print s	
	#print mang
	if u not in mang1:
		if int(u)%1==0:
			print s
			process_insert(s)
			if int(u)%1==0:
				process_update(s)				
		if u == 59:
			del mang1[:]
		else :		
			mang1.append(u)


def run():
	while(True):
		checktime()

run()
print "End: "+str(datetime.datetime.now())
