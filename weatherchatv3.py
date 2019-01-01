import sys
sys.path.append('/home/pi/iot-ts')
import json
import time
from time import sleep
import urllib.request
import logging
import subprocess
from subprocess import call
import string
from sense_hat import SenseHat
sense = SenseHat()




#as request is only available in pthon3, this file has to be run with this syntax python3 weatherchatv3.py 

todayweather = "false"
greetN = ""
weatherUpd = ""

names = ["Majella","Martin","Tommy"]

# MAC addresses of devices
macs = ["C4:61:8C:39:66:E0","60:A1:0A:4D:FF:B7","59:xx:xx:xx:xx:xx"]

api="Z6vAk7sGMhxBi1cB9GirChVzAAnvRNKG"
location_id="1078838"
#1078838 is the code AccuWeather code for wellingtonbridge, near where i live
#current conditions  returns a field called  has precipitation which is either true or false
NOT_RAIN = " Its not raining" 
RAIN =" Its Raining, bring an umbrella"
raining = ""




def get_weather(api, location_id):
    url = 'http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true' % (location_id, api)
    with  urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print(data[0]['HasPrecipitation'])
    if str(data[0]['HasPrecipitation']) == "False":
        global raining
        global NOT_RAIN
        raining = NOT_RAIN
    else:
        global RAIN
        global raining
        raining = RAIN

    tempp = (data[0]['Temperature']['Metric']['Value'])
    wtext = (data[0]['WeatherText'])
    weather = 'It is %s degrees celcius  and its %s. Is it Raining ? %s today.' %(tempp,wtext,raining) 
    global todayweather
    todayweither = "true"
    return weather



def arp_scan():
     try:
        output2 = subprocess.check_output("sudo arp-scan -l", shell=True)
          
        if len(output2) > 0:
          for i in range(len(names)):
                    # when run as python3  needed to encode rather than using str()
                    if macs[i].encode('utf-8') in output2.upper():
                       print(names[i] + "'s device is present")
                       global greetN
                       greetN = names[i] + ", "
     except Exception as e:
            logging.error(e)





def speaktome(inputcommand):
    try:
       p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
       (output, err) = p.communicate()
       return output
    except Exception as e:
        logging.error(e)




#program begins with a ARP-Scan
ii =4
while len(greetN) == 0:
  arp_scan()
  ii = ii -1
  sleep(5)
  if  ii == 0:
   break


# as i only have limited  number of requests per day i am limiting the request to one, when the program is run, and when  there is a recognised person scanned
if (todayweather == "false") and (len(greetN) > 0 ):
     global weatherUpd
     weatherUpd= get_weather(api, location_id)


result = "Good Morning ," + greetN
greetMe="espeak 'Good Morning {} this is Pi. {}' -ven-us+m3 -p40 -s120 --stdout | aplay -D bluealsa:HCI=hci0,DEV=60:4E:AC:4E:37:24,PROFILE=A2DP".format(greetN,weatherUpd)


if len(greetN) > 0:
   sense.show_message(result)
   speaktome(greetMe)



