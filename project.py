import serial
import urllib2
import urllib
import time
import datetime
import pymysql as sql

d = open("../addr/addr.txt",'r')
address = []
while True : 
	addr = d.readline().replace('\n','')
	if not addr: break
	address.append(addr)

conn = sql.connect(host = address[0] , user = address[1] , password = address[2] , db = address[3] , charset = address[4])
curs = conn.cursor()

try :
	global ser 
	ser = serial.Serial('/dev/ttyUSB0', 9600) # connection with arduino using 485
	global url 
	url = 'http://192.168.0.14:9900/data' # address of server
except serial.SerialException as e: 
	print("check the USB port")

def fileSave(data) :
	#now = datetime.datetime.now().strftime('%y%m%d %H%M%S')
	with open("../data/data.txt",'a') as f : # save data in a folder named 'data'
		f.write(str(data) + '\n')

def dbSave(data) :
	query = "Insert into data(device_No, temperature, humidity,time) values (%s,%s,%s,now());"
	query = "Insert into data(temperature, humidity, time) values (%s,%s, now());"
	curs.execute(query, (data['temperature'],data['humidity']))
	conn.commit() # use commit if db can be applied	


def readData() :
	try :
		data = (ser.readline()) #read data from arduino
		data = data.replace('\n','').replace('\r','')
		data = data.split(' ')
		data = {'device_No': int(data[0]),'temperature': float(data[1]), 'humidity': float(data[2])}
		now = datetime.datetime.now().strftime('%y%m%d %H%M%S')
		data['time'] = now
		dbSave(data)
		fileSave(data) #save data immediately
		print (data)
		return (data)
	except IndexError as e:
		print(e)
		readData()
	


def trsData() :
	while True :
		th = urllib.urlencode(readData())
		req = urllib2.Request(url, data= th)
		res = urllib2.urlopen(req)
		d = res.read()
		print(d)
		time.sleep(0.5)

#trsData()
while True :
	readData()

conn.close()
