# Created by Harjas Singh Anand

import streams
import json
from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver
from aws.iot import iot
import helpers
pinMode(2,OUTPUT)
new_resource('private.pem.key')
new_resource('certificate.pem.crt')
new_resource('thing.conf.json')

def shadow_callback(requested):
    global publish_period
    print('requested publish period:', requested['publish_period'])
    publish_period = requested['publish_period']
    return {'publish_period': publish_period}
ser2 = streams.serial(SERIAL2)
#ser2 = streams.serial()
wifi_driver.auto_init()

print('connecting to wifi...')
i=5
while(i):
    digitalWrite(2, HIGH)  
    sleep(100)               
    digitalWrite(2, LOW)  
    sleep(100)
    i-=1
#Enter Wifi Name and Password here:
wifi.link("STUXNET",wifi.WIFI_WPA2,"telnet#202928")
digitalWrite(2, HIGH)
pkey, clicert = helpers.load_key_cert('private.pem.key', 'certificate.pem.crt')
thing_conf = helpers.load_thing_conf()
publish_period = 1000

thing = iot.Thing(thing_conf['endpoint'], thing_conf['mqttid'], clicert, pkey, thingname=thing_conf['thingname'])
print('connecting to mqtt broker...')
thing.mqtt.connect()
thing.on_shadow_request(shadow_callback)
thing.mqtt.loop()

thing.update_shadow({'publish_period': publish_period})


while True:
    len = ser2.available()
    if len > 0:
        line = ser2.readline("\u0004")
        print('Data received from Machine...')
        print('Data sent to server..')
        print(a)
        thing.mqtt.publish("dev/sample", json.dumps({"Data":line}))
    sleep(publish_period)
    
    
    
       


