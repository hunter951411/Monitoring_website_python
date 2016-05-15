from selenium import webdriver
from PIL import Image
def screenshot(url,s):
	browser = webdriver.Firefox()
	urlfull = "http://"+url+"/"
	#print urlfull
	browser.get(urlfull)
	name = "Test1/Pictures/"+url+".png"
	#print name
	browser.save_screenshot(name)
	browser.quit()
	img = Image.open(name)
	img1 = img.crop((0, 0, 1000, 800))
	img1.save(name)
	return name
