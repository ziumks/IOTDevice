import urllib2
import urllib
import Adafruit_DHT as dht
import time

url = 'http://192.168.0.14:9900/data'

def trsData():
	while True :
		th = urllib.urlencode(readData())
		req = urllib2.Request('http://192.168.0.14:9900/data',data = th)
		res = urllib2.urlopen(req)
		d = res.read()
		print(d)
		time.sleep(0.5)



def readData(): #read temperature, humidity from DHT11
	h,t = dht.read_retry(dht.DHT11,4) #read data from gpio N(In this, N is 4)
	data = {'temperature':t,'humidity': h }
	return(data) #only one of thing can be return. So dictionary is easy to use 	


trsData()
