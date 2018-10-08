from time import sleep
import Adafruit_DHT
import Adafruit_DHT as dht

sensor = Adafruit_DHT.DHT22
pin = 5

h,t = dht.read_retry(dht.DHT22, 5)

print ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
