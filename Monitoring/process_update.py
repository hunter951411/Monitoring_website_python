from screenshot import screenshot
from run_update import run_update
import mysql.connector
from threading import Thread
import time
mang = []
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
		                password='trung',database='demo2')

c = conn.cursor()
def process_update(s):
	print "mang update"
	print mang
	del mang[:]
	print mang
	find ="Select Url from updatetable"
	c.execute(find)
	for row in c:
			mang.append(row[0])
	#conn.commit()
	print mang
	for x in mang:
    		run_update(x,s)	
	#for x in mang:
	#	#screenshot(x)
	#	if (run_update(x,s)==2):
	#		break
	
	#	else:
	#		Thread(target=screenshot, args=(x,s)).start()
	#		time.sleep(2)
		#print x
	#time.sleep(40)
		#print x
		#Thread(target=run_update, args=(x,s,)).start()
		#time.sleep(1)
