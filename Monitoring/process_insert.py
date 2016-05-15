from run_insert import run_insert
from threading import Thread
import mysql.connector
mang = []
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
		                password='trung',database='demo2')

c = conn.cursor()
def process_insert(s):
	print "Mang insert"
	print mang
	del mang[:]
	#print mang
	find ="Select Url from updatetable"
	c.execute(find)
	for row in c:
		#print (row[0])		
		mang.append(row[0])

	for x in mang:
		run_insert(x,s)
		#print x
		#Thread(target=run_insert, args=(x,s,)).start()
		#time.sleep(1)

