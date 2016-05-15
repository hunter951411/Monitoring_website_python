import subprocess
import re
import datetime
import socket
def ping_time(url):
	try:
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
			Timeresult = 0
		else:
			if int(ReceiveResult[0])== 0:
				print "ping failed"
				Timeresult = 0	
			elif int(ReceiveResult[0])== 1:
				Timeresult = Time[0]
	except:
		Timeresult = 0
	return Timeresult

def get_ip(url):
	try:	
		ip = socket.gethostbyname(url)
	except:
		ip = ''
	return ip
