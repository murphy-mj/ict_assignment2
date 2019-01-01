import sys
sys.path.append('/home/pi/iot-ts')
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
import time
from datetime import datetime 
import datetime
import json

#getting todays and yesterdays day of the month
today = datetime.date.today()
tday = today.day
yday = tday - 1


#create DB to store home times
db = TinyDB('mydb.json')

#creating a query object
myDBQuery= Query()


#routine to display all items inn the db file
def printAllItems():
   allItem =""
   for item in db:
       allItem = allItem +  item['user'] + item['time'] +"\n"
   return allItem


#routine to display martin earliest time returning home
def earlyTime():
    result = db.search((myDBQuery.user == "Martin") & (myDBQuery.day == tday))
    result2 = min(result)
    return result2


def earlyTimeTime():
    result = db.search((myDBQuery.user == "Martin") & (myDBQuery.day == tday))
    result2 = min(result)
    result3 = result2['time']
    tt = str(datetime.datetime.strptime(result3,'%Y-%m-%dT%H:%M:%S.%f').strftime("%X")) 
    return tt




#routine to display martin latest time returning home
def latestTime():
    result = db.search((myDBQuery.user == "Martin") & (myDBQuery.day == tday))
    result2 = max(result)
    return result2


#add new entry to db file
def addEntry(mac,user,tme,d):
     db.insert({"macid":mac,"user":user,"time":tme,"day":d})

#print(latestTime())
