import mysql.connector
#login vao csdl mysql
conn = mysql.connector.Connect(host='127.0.0.1',user='root',password='trung')
c = conn.cursor()
#Tao database
sql = "CREATE DATABASE IF NOT EXISTS MonitoringDB"
c.execute(sql)
conn.commit()
#Su dung database vua tao ra
sql = "USE MonitoringDB"
c.execute(sql)
conn.commit()
#Tao table inserttable
sql = """CREATE TABLE IF NOT EXISTS inserttable (
        Ids        int        primary key not NULL AUTO_INCREMENT,
	Url	varchar(30),
	PingTime	float,
	GetTime		float,
	Active		boolean,
	Time	datetime)"""
c.execute(sql)
conn.commit()

#Tao bang updatetable
sql = """CREATE TABLE IF NOT EXISTS updatetable (
        Ids        int        primary key not NULL AUTO_INCREMENT,
	Url	varchar(30),
	Ip	varchar(30),
	LastPingTime	float,
	LastGetTime	float,
	Picture		longblob,
	Active	boolean,
	MailReport	varchar(50),
	LastTime	datetime)"""
c.execute(sql)
conn.commit()

#Insert du lieu vao bang updatetable
c.execute("""Insert into updatetable values(1,'www.dantri.com.vn','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(2,'www.24h.com.vn','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(3,'www.vtc.vn','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(4,'www.askubuntu.com','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(5,'www.stackoverflow.com','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(6,'www.baomoi.com','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(7,'www.vnexpress.net','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
c.execute("""Insert into updatetable values(8,'www.thanhnien.vn','192.168.1.1',6.12,6.12,'',0,'hunter141195@gmail.com','')""")
conn.commit()
#Kiem tra cac cot trong bang inserttable
sql = "SHOW COLUMNS FROM inserttable"
c.execute(sql)
for row in c:
	print (row)
conn.commit()
#Kiem tra cac cot trong bang updatetable
sql = "SHOW COLUMNS FROM updatetable"
c.execute(sql)
for row in c:
	print (row)
conn.commit()