#thingspeak & mac address 

import paho.mqtt.publish as publish
import string
import sys
sys.path.append('/home/pi/iot-ts')
import dbreview
from time import sleep
import logging
import subprocess
import json
import time
import datetime
from wia import Wia
from subprocess import call
from sense_hat import SenseHat
sense = SenseHat()

#wia not fnctioning presently

#creating a wia object
#wia = Wia()
#wia.access_token = "d_sk_CMDFLpqYOJibFZj1sNfB7eq6"


#thingspeak set up
# The ThingSpeak Channel ID.
channelID = "655701"

# The Write API Key for the channel.
writeAPIKey = "3N69QEFU2A8B41JN"

# The Hostname of the ThingSpeak MQTT broker.
mqttHost = "mqtt.thingspeak.com"

mqttUsername = "usr martin"

# Your MQTT API Key from Account > My Profile.
mqttAPIKey ="AALCI1A6E9VG8210"

tTransport = "websockets"
tPort = 80

# Create the topic string.
topic = "channels/" + channelID + "/publish/" + writeAPIKey


#create DB to store home times
#this is done through the python file dbreview




#Names of device owners
names = ["Majella","Martin","Tommy"]
# MAC addresses of devices
macs = ["C4:61:8C:39:66:E0","60:A1:0A:4D:FF:B7","59:xx:xx:xx:xx:xx"]

greetN = ""
macN = ""
result =""

#these fields indicate if martin, majella or tommy are home
field1 = False
field2 = False
field3 = False
#filed 4 is the time that martin returned
field4 = ""




def speaktome(inputcommand):
    try:
       p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
       (output, err) = p.communicate()
       return output
    except Exception as e:
        logging.error(e)

#setting variable to true, if person is home
def isHome(i):
     try:
        if i == 1:
           global field1
           field1 = True
        elif i == 2:
           global field2
           field2 = True
        elif i == 3:
           global Field3
           field3 = True

     except Excetion as e:
        loging.error(e) 


def whosHome(person,tme):
   try:  
     global field1
     global field2
     if person == "Martin" and field1 == "false":
        #wia.Event.publish(name="calling",data=tme)
        print("home")
     if person == "Majella" and field2 == "false":
        print("Home2")
        #wia.Event.publish(name="calling2",data=tme)
   except exception as e:   
      logging.error(e)


def arp_scan():
     try:
        output2 = subprocess.check_output("sudo arp-scan -l", shell=True)

        for i in range(len(names)):
                if macs[i] in output2.upper():
                    print(names[i] + "'s device is present")
                    # with each scan record in DB
                    dbreview.addEntry(macs[i],names[i],datetime.datetime.now().isoformat(),datetime.date.today().day)
                    global greetN
                    greetN = names[i] + ", "
                    whosHome(names[i],datetime.datetime.now().isoformat())
                    isHome(i)
		else:
                    print(names[i] + "'s device is NOT present")
     except Exception as e:
            logging.error(e)


def blue_scan():
     try:
        output2 = subprocess.check_output("sudo hcitool scan", shell=True)

        for i in range(len(names)):
                if macs[i] in output2.upper():
                    print(names[i] + "'s device is present")
                    #with each scan record in DB
                    dbreview.addEntry(macs[i],names[i],datetime.datetime.now().isoformat(),datetime.date.today().day)
                    global greetN
                    greetN = names[i] + ", "
                    whosHome(names[i],datetime.datetime.now().isoformat())
                    isHome(i)

                else:
                    print(names[i] + "'s device is NOT present")
     except Exception as e:
            logging.error(e)




#while True:

ii  = 4
# going to run this prog through cron, and  it will loop and sleep for 15 minutes intervals

#while(ii > 0):
while len(greetN) ==0:
  blue_scan()
  global greetN
  if len(greetN) == 0:
      arp_scan()
 
  if len(greetN) > 1:
       global greetN
       global macN
       global result
       result = "welcome home ," + greetN
       sense.show_message(result)
       greetMe="espeak 'Welcome {} this is Pi.  I hope you had a pleasant day ' -ven-us+m3 -p40 -s120 --stdout | aplay -D bluealsa:HCI=hci0,DEV=60:4E:AC:4E:37:24,PROFILE=A2DP".format(greetN)
       speaktome(greetMe)
 
  sleep(5)
  if ii == 0:
    break
  ii = ii -1





#on exit publish the arrival time of Martin that day.

field4time=""
payload2=""
print(dbreview.earlyTimeTime())
field4time =dbreview.earlyTimeTime()
payload2 = "field1="+str(field1) + "&field4="+str(dbreview.earlyTimeTime())


try:
  publish.single(topic, payload2, hostname=mqttHost, transport=tTransport, port=tPort,auth={'username':mqttUsername,'password':mqttAPIKey})
  print ("Martin arrived home at ",field4time," to host: " , mqttHost)
except:
   print ("There was an error while publishing")

print("Good Bye")

