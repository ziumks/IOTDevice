import serial
import urllib2
import urllib
import time
import datetime
import pymysql as sql

conn = sql.connect(host = '192.168.0.14', user = 'pi', password = 'ziumks00', db = 'ZiumIOT' , charset = 'utf8')
curs = conn.cursor()


ser = serial.Serial('/dev/ttyUSB0', 9600) # connection with arduino using 485
url = 'http://192.168.0.14:9900/data' # address of server

def fileSave(data) :
	now = datetime.datetime.now().strftime('%Y%M%D %H%M%S')
	with open("../data/data.txt",'a') as f : # save data in a folder named 'data'
		f.write(str(now) + str(data) + '\n')

def dbSave(data) :
	query = "Insert into data(temperature, humidity) values (%s,%s);"
	curs.execute(query, (data['temperature'],data['humidity']))
	conn.commit()	


def readData() :
	data = (ser.readline()) #read data from arduino
	data = data.replace('\n','').replace('\r','')
	data = data.split(' ')
	data = {'temperature': float(data[0]), 'humidity': float(data[1])}
	dbSave(data)
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

conn.close()
