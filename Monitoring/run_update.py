from get_time import get_time
from ping_time import ping_time
from ping_time import get_ip
import mysql.connector
conn = mysql.connector.Connect(host='127.0.0.1',user='root',\
		                password='trung', database='demo2')

c = conn.cursor()
def run_update(url,s):
	Active = get_time(url)[1]	
	update ="Update updatetable set Ip='"+str(get_ip(url))+"', LastPingTime='"+str(ping_time(url))+"', LastGetTime='"+str(get_time(url)[0])+"',LastTime='"+str(s)+"',Active='"+str(Active)+"' Where Url='"+url+"'"
	try:
		c.execute(update)
		conn.commit()
		print update
	except Exception,e: 
		print str(e)
	return	Active
