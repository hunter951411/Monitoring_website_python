from get_time import get_time
from ping_time import ping_time
import mysql.connector
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
		                password='trung',database='demo2')

c = conn.cursor()
def run_insert(url,s):
	Active = get_time(url)[1]
	insert ="Insert into inserttable(Url,PingTime,GetTime,Active,Time) Values('"+str(url)+"', '"+str(ping_time(url))+"', '"+str(get_time(url)[0])+"',"+str(Active)+",'"+str(s)+"')"
	try:
		c.execute(insert)
		#c.execute(insert)
		conn.commit()
		print insert
	except Exception,e: 
		print str(e)
