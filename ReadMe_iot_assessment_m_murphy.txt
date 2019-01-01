Student Name: Martin Murphy
Student Id: 246587
Course:Higher Diploma in Computer Studies 2018/19
Assigment:Computer Systems and Networks, Assessment2. Iot Application

"https://github.com/murphy-mj/ict_assignment2"


Hi Frank,
The original idea was to be able to see the time that a mac entered a space  and 
then look frequency and patterns.
 
The issue i found that the hcitoot scan will only pick up devices that have their bluetooth Discoverable setting set to True.
But this only last for 120 seconds on my phone (which is an old phone and not very smart), so the scan will never find many/any devices
There a kali linux image file and using a hcitool scan and a programe called Bluesnarfer, 
one can not only extract the phones mac, but read the phone simm card and make calls. 
I did not feel comfortable going don that raod, so i decided that i was happy withn the arp scan.

I concentrated on using the address of my phone mac and my wife's majellas and worked with that. 

i have created 3 python files,
1. dbreview.py file used to create of a Tinydb file and methods to work with the database created. This file/module will be imported into 
the main file "ts-wia-publish_Assign.py"
2. weatherchatv3,is the second file created, which will be ran in the morning.
The scan determines if majella or I are connected. If so, it then uses the accuweather api, to ascertain the current weather conditions.
I have registered with the organisation and received a secrity key and ascertained the location of my nearest village.
Then using bluetooth and the espeak package, a greeting is created and included are facts relating to the weather.
It will also display a good morning message on the sense hat.
3. ts-wia-publish_Assign.py, file will be ran in the afternoon.
The scans, one using the arp and the other using hcitool scan, dtermines who is home.It will also display a good afternoon message on the sense hat. If it finds either majella or I, is at home it send an event notification to wia. One Event for Majella, calling2, and one for me, calling. This information is stored in  the Tinydb. I was unable to connect the events to logic, wia's flow, so uable to do any action.
Before the program ends, two events are created in ThingsSpeak,
one event, based on method in thr  is used to create a graph of my home times, 
the other, is used as a trigger for an action, which sends a tweet to my new twitter account.


general note, i have used "global" in relation to variables alot in my programs, not 100 sure i am correct, but from what i understand
if you use a variable within a method, it assumes it a local variable, so global tells the method to use the main variable/global. 

used crontab to schedule the 2 python files.
the weatherchatv3 needs to be called using python3, due to the use of .request in the file


Kind Regards Martin

==== 

BLUETOOTH:

in order to set up the speaker we carry out the folowing activites.

pi@raspberrypi:~/iot-ts $ bluetoothctl
Agent registered
[bluetooth]# scan on
Discovery started
[CHG] Controller B8:27:EB:28:BF:EE Discovering: yes
[CHG] Device 60:4E:AC:4E:37:24 RSSI: -59
[CHG] Device 60:4E:AC:4E:37:24 ManufacturerData Key: 0x544d
[CHG] Device 60:4E:AC:4E:37:24 ManufacturerData Value:
  00 00 01 fe 58                                   ....X
[bluetooth]# connect 60:4E:AC:4E:37:24
Attempting to connect to 60:4E:AC:4E:37:24
[CHG] Device 60:4E:AC:4E:37:24 Connected: yes
Connection successful
[CHG] Device 60:4E:AC:4E:37:24 ServicesResolved: yes
[A58077]# exit

this can be achieved by setting a line in the /etc/rc.local file, so when the raspberry is turned on, it will connect to the speaker.
echo 'connect 60:4E:AC:4E:37:24 \n quit' | bluetoothctl


volume control, at command line
amixer -D bluealsa sset "A58077 - A2DP" 50%

Simple mixer control 'A58077 - A2DP',0
  Capabilities: pvolume pswitch
  Playback channels: Front Left - Front Right
  Limits: Playback 0 - 127
  Mono:
  Front Left: Playback 64 [50%] [on]
  Front Right: Playback 64 [50%] [on]


i have used Espeak for the voice package,
the message is piped to aplay with the required parameter. 

"espeak 'Welcome {} this is Pi.  I hope you had a pleasant day ' -ven-us+m3 -p40 -s120 --stdout |
  aplay -D bluealsa:HCI=hci0,DEV=60:4E:AC:4E:37:24,PROFILE=A2DP".format(greetN)
 
I found these tutorials usedful.
Baby Bluetooth Steps on Raspberry Pi3 - Raspbian (Stretch),
Raspberry Pi zero W Bluetooth speaker connection voice,
RPi Test to Speech (Speech Synthesis).
i wont mention the longer list, that did not help.



Tinydb:

the Tinydb database created in the file called dbreview.py.
In this file i created a number of methods to work with the data stored

#create DB to store home times
db = TinyDB('mydb.json')

#creating a query object
myDBQuery= Query()


#add new entry to db file
def addEntry(mac,user,tme,d):
     db.insert({"macid":mac,"user":user,"time":tme,"day":d})

# this returns the earlest time i connected to the wifi or was in bluetooth discoverable mode
def earlyTimeTime():
    result = db.search((myDBQuery.user == "Martin") & (myDBQuery.day == tday))
    result2 = min(result)
    result3 = result2['time']
    tt = str(datetime.datetime.strptime(result3,'%Y-%m-%dT%H:%M:%S.%f').strftim$
    return tt

I had difficulty using the datetime object with in the search, so in the end i saved the day separately in the json object, 
then created a number of variables tday,yday to use in the search. Not ideal. 



Wia/ThingSpeak

An account has been set up at ThingSpeak and Wia.
Wia has been difficult, while it was initially possible to send events, it was not possible to use the Flow, as it would not join the elemnts together.  I sent an email to the company, i believe that its a combination of Windows 10 and using Chrome, that is causing the issue. The help desk, conall, was very helpful, and 'fixed' the issue. However, when i tried to use it, i could not any post events, but the flow was working. So decided to comment the wia sections out.

The ThingSpeak, i use is to send my arrival time and to graph this.
and another event to trigger a tweet to my twiter a/c.

wia space
spc_lL1D1brG


Kind Regards Martin.

 


 




