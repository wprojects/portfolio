import time
import mysql.connector as mysql
import requests
import json
from datetime import date, datetime, timedelta, timezone



mydb = mysql.connect(host="neodbinstance.cqieshqdcqmd.us-east-2.rds.amazonaws.com",user="neoadmin",password="mycelium1",database="neodb")
# Truncate table to populate it with fresh data from API
mycursor = mydb.cursor()
sql = "TRUNCATE TABLE map_leads_hex"
mycursor.execute(sql)
mydb.commit()
mycursor.close()
mydb.close()

url = "https://api.helium.io/v1/hotspots/location/box?swlat=35.403115&swlon=-94.424047&nelat=36.479715&nelon=-93.363866"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload).json()
for item in response['data']:
    # print(f"{item['name']}, {item['lng']}, {item['lat']}")
    hex = item['location_hex']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = mysql.connect(host="neodbinstance.cqieshqdcqmd.us-east-2.rds.amazonaws.com",user="neoadmin",password="mycelium1",database="neodb")
    mycursor = mydb.cursor()
    hex = item['location_hex']
    # print(hex, ' = test hex')
    # sql = "insert into map_leads_hex (hex) values (%s)"
    # val = (hex)
    sql="INSERT INTO map_leads_hex (hex, accessed) values (%s, %s)"
    mycursor.execute(sql, (hex, timestamp))
    # mycursor.execute(sql,val)
    mydb.commit()
    mycursor.close()
    mydb.close()
    # print("All nodes successfully verified in --- %s seconds ---" % (time.time() - start_time))
    print('Finished storing og map data')

    # print('yo')
cursor = response['cursor']

list_of_coordinates = []

############Right here you can save the dat from the previous request to a list or something#####################


while True:
    time.sleep(.5)
    url = f"https://api.helium.io/v1/hotspots/location/box?swlat=35.403115&swlon=-94.424047&nelat=36.479715&nelon=-93.363866&cursor={cursor}"
    response = requests.request("GET", url, headers=headers, data=payload).json()
    for item in response['data']:
        # print(f"{item['name']}, {item['lng']}, {item['lat']}")
        hex = item['location_hex']
        print(f"{hex}")
        # print('yo')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        mydb = mysql.connect(host="neodbinstance.cqieshqdcqmd.us-east-2.rds.amazonaws.com",user="neoadmin",password="mycelium1",database="neodb")
        mycursor = mydb.cursor()
        hex = item['location_hex']
        # print(hex, ' = test hex')
        # sql = "insert into map_leads_hex (hex) values (%s)"
        # val = (hex)
        sql="INSERT INTO map_leads_hex (hex, accessed) values (%s, %s)"
        mycursor.execute(sql, (hex, timestamp))
        # mycursor.execute(sql,val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        # print("All nodes successfully verified in --- %s seconds ---" % (time.time() - start_time))
        print('Finished storing map data')

    # ###########Save data#####################

    try:
        cursor = response['cursor']
        # print(cursor)
    except KeyError:
        break





print("All locations found!!")