def config_d():
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

