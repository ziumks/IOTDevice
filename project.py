import serial
import urllib2
import urllib
import time
import datetime

ser = serial.Serial('/dev/ttyUSB0', 9600) # connection with arduino using 485
url = 'http://192.168.0.14:9900/data' # address of server

def fileSave(data) :
	now = datetime.datetime.now().strftime('%Y%M%D %H%M%S')
	with open("../data/data.txt",'a') as f : # save data in a folder named 'data'
		f.write(str(now) + str(data) + '\n')



def readData() :
	data = (ser.readline()) #read data from arduino
	data = data.split(',')
	data = {'temperature':data[0],'humidity':data[1]}
	fileSave(data) #save data immediately
	return (data)


def trsData() :
	while True :
		th = urllib.urlencode(readData())
		req = urllib2.Request(url, data= th)
		res = urllib2.urlopen(req)
		d = res.read()
		print(d)
		time.sleep(0.5)

trsData()

