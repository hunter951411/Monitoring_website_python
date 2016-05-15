import datetime
import mysql.connector
import time
from process_insert import process_insert
from process_update import process_update
mang1 = []
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
		                password='trung',database='demo2')

c = conn.cursor()
def checktime():
	i = datetime.datetime.now()
	u = int(i.strftime('%S'))
	s = i.strftime('%Y-%m-%d %H:%M:%S')
	#print s	
	#print mang
	if u not in mang1:
		if int(u)%1==0:
			process_insert(s)
			if int(u)%59==0:
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
