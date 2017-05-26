import socket
import subprocess
import re
import datetime
import httplib
from selenium import webdriver
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
import timeit
#Khai bao cac thong so mail va dang nhap vao mail de bao cho mail Admin
server = smtplib.SMTP()
EMAIL_ACCOUNT = "Bcct28042016@gmail.com"
EMAIL_PASS = "HelloVietNam"
server.connect('smtp.gmail.com', port = 587) 
server.ehlo()
server.starttls()
server.login(EMAIL_ACCOUNT, EMAIL_PASS)

#Ket noi vao csdl
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
                        password='trung',database='MonitoringDB')
c = conn.cursor()

#Nhan thong tin ping
def Ping_Time(url):
	ping = subprocess.Popen(["ping", "-c", "1", url],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	i = datetime.datetime.now()
	s = i.strftime('%Y-%m-%d %H:%M:%S')
	out, error = ping.communicate()
	regexIp = "\s?\((.+?)\)\s?"
	Ip = re.findall(regexIp, out)
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

#Nhan thong tin get
def Get_Time(url):
	try:
		start_time = timeit.default_timer()
		connect_get = httplib.HTTPConnection(url)
		connect_get.request("GET", "/")
		elapsed = timeit.default_timer() - start_time
		r1 = connect_get.getresponse()
		intr1status = (int(r1.status))/100
	except:
		intr1status = 0
	if (intr1status == 5 or intr1status == 4):
		#Neu get khong thanh cong gan bien status = 1 de Set trang thai cua website Active la OFF
		status = 1
		#Tim kiem Mail cua Admin va gui thong bao
		find ="Select MailReport from updatetable where Url='"+url+"'"
		c.execute(find)
		for row in c:
			timedie = datetime.datetime.now()		
			Send_Mail(timedie,row[0])	
		conn.commit()
	elif(intr1status == 0):
		#Neu get khong thanh cong gan bien status = 2 de khong thuc hien Update vao csdl
		status = 2
		#Tim kiem Mail cua Admin va gui thong bao
		find ="Select MailReport from updatetable where Url='"+url+"'"
		c.execute(find)

		for row in c:
			timedie = datetime.datetime.now()		
			Send_Mail(timedie,row[0])
		conn.commit()
	else:
		status = 0 #Status  = 0 nghia la trang thai cua website Active la ON
	#Thuc hien chuyen thoi gian get sang mileseconds	
	timeget = float(elapsed * 1000)
	timeget = timeget * 100
	timeget = int(timeget)
	timeget = float(timeget)/100
	
	return float(timeget),status

#Ham thuc hien gui mail cho Admin cua Server chua url, voi tham so truyen vao la thoi gian url chet: timedie
# va mail cua Admin: mailreport
def Send_Mail(timedie, mailreport):
	fromaddr = "Monitoring Report"
	msg = email.MIMEMultipart.MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = email.Utils.COMMASPACE.join(mailreport.split())
	msg['Subject'] = "Website Status" 
	msg.attach(MIMEText("Website die in "+ str(timedie)))
	msg.attach(MIMEText('nsent via python', 'plain')) 
	server.sendmail(EMAIL_ACCOUNT,mailreport.split(),msg.as_string())


#chup anh website
def Screenshot(url):
	name_pic = "Pictures/"+url+".png"
	src = os.system("webkit2png -o "+name_pic+" -g 1000 600 http://"+url+"/")
	return name_pic

#Ham lay dia chi ip cua url
def Get_Ip(url):
	return socket.gethostbyname(url)

#Ham thuc hien update du lieu vao csdl
def Run_Update(url,time):
	Active = Get_Time(url)[1]	
	update ="Update updatetable set Ip='"+str(Get_Ip(url))+"', LastPingTime='"+str(Ping_Time(url))+"', LastGetTime='"+str(Get_Time(url)[0])+"', Picture='"+"Pictures/"+url+".png"+"',LastTime='"+str(time)+"',Active='"+str(Active)+"' Where Url='"+url+"'"
	print update
	c.execute(update)
	conn.commit()
	return	Active 	

#Ham thuc hien insert du lieu vao csdl
def Run_Insert(url,time):
	Active = Get_Time(url)[1]
	insert ="Insert into inserttable(Url,PingTime,GetTime,Active,Time) Values('"+str(url)+"', '"+str(Ping_Time(url))+"', '"+str(Get_Time(url)[0])+"',"+str(Active)+",'"+str(time)+"')"
	print insert
	c.execute(insert)
	conn.commit()

#Ham thuc hien Update du lieu vao bang Update
MANG_URL = []
def Process_Update(time):
	del MANG_URL[:]
	find ="Select Url from updatetable"
	c.execute(find)
	for row in c:
		MANG_URL.append(row[0]) #Lay tat ca cac url trong bang update va them vao MANG_URL (dang rong)
	#Tien trinh thuc hien goi den ham Run_Update de update du lieu vao bang update dung thread	
	conn.commit()
	for url in MANG_URL:
		if (Run_Update(url,time)==2):
			break		
		else:
			Screenshot(url) 
			#Thread(target=Screenshot, args=(url,)).start()	#Luong thuc hien chup trang thai website tai thoi diem thuc hien
			# Thread(target=Run_Update, args=(url,time,)).start() #Luong thuc hien update du lieu vao bang Update
			Run_Update(url, time)

#Ham thuc hien insert du lieu vao bang Insert
def Process_Insert(time):
	del MANG_URL[:]
	find ="Select Url from updatetable"
	c.execute(find)
	for row in c:	
		MANG_URL.append(row[0])
	conn.commit()	
	for url in MANG_URL:
		# Thread(target=Run_Insert, args=(url,time,)).start() #Luong thuc hien insert du lieu vao bang Insert
		Run_Insert(url,time)

#Ham Run_Checktime thuc hien kiem tra thoi gian de thuc hien cac tien trinh
MANG_THOIGIAN = []	#Mang chua thoi gian troi qua trong 1 tieng
def Run_Checktime():
	timecurr = datetime.datetime.now()	#Bien timecurr la thoi gian hien tai
	timecurr_second = int(timecurr.strftime('%M')) #Bien timecurr_second chi so phut hien tai
	time_insert = timecurr.strftime('%Y-%m-%d %H:%M:%S') #Bien time_insert thuc hien day vao ham 
												#process_update va process_insert sao cho thoi gian dong bo
	if timecurr_second not in MANG_THOIGIAN:
		if int(timecurr_second)%1 == 0:
			print time_insert			#Thuc hien kiem tra thoi gian de cach 5p insert vao csdl 1 lan 
			Process_Insert(time_insert)
			if int(timecurr_second)%2==0:		#Thuc hien kiem tra thoi gian de cach 10p update vao csdl 1 lan
				Process_Update(time_insert)				
		if timecurr_second == 59:				#1 tieng troi qua thuc hien xoa mang thoi gian va quet tiep
			del MANG_THOIGIAN[:]
		else :		
			MANG_THOIGIAN.append(timecurr_second) # Neu so phut hien tai chua co trong MANG_THOIGIAN thi them vao

#Ham chinh thuc hien chay chuong trinh
def main():
	while(True):
		Run_Checktime()

#Goi den ham chinh de chay chuong trinh
main()
