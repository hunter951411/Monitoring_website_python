import datetime
import httplib
from send_mail import send_mail
import time
import mysql.connector
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
		                password='trung',database='demo2')

c = conn.cursor()

def get_time(url):
	try:	
		startget = datetime.datetime.now()	
		try:
			conn = httplib.HTTPConnection(url)
			conn.request("GET", "/")
			r1 = conn.getresponse()
			endget = datetime.datetime.now()
			gettimeinsert = (endget-startget)
			intr1status = (int(r1.status))/100
		except:
			intr1status =0
		if (intr1status == 5 or intr1status == 4):
			status = 1
			find ="Select MailReport from updatetable where Url='"+url+"'"
			c.execute(find)
			for row in c:
				send_mail(startget,row[0])	
		elif(intr1status == 0):
			status = 2
			find ="Select MailReport from updatetable where Url='"+url+"'"
			c.execute(find)
			for row in c:
				#print (row[0])		
				send_mail(startget,row[0])
		else:
			status = 0
		conn.close()
		timeget = float(gettimeinsert.total_seconds() * 1000)
		timeget = timeget * 100
		timeget = int(timeget)
		timeget = float(timeget)/100
	except:
		timeget = 0
		status = 1	
	return float(timeget),status
