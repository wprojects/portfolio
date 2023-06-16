import time
import requests
import json
from datetime import date, datetime, timedelta, timezone
import mysql.connector as mysql
import datetime as dt
import os
from dotenv import load_dotenv
from pathlib import Path
import requests as r
import aiohttp
import backoff
import http.client


load_dotenv()
env_path = Path('/home/samwins/quantum/')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']


# Globals ---
mydb = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)


@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
    return response


########################## SQL queries ##########################
#CRM Record Queries
check_hex_overflow = "select hex from hex_data"
#DB Data Pull Queries
#Insert Queries
insert_hex_data = "INSERT INTO hex_data (hex, accessed) values (%s, %s)"
#Truncate Queries
truncate_hex_data = "TRUNCATE TABLE hex_data"

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)

def run_query(statement, args = None):
    cursor = zohoDB.cursor()
    cursor.execute(statement, args)

    if "select" == statement.split()[0]:
        result = cursor.fetchall()
        cursor.close()
        return result
    else:
        zohoDB.commit()
        cursor.close()

run_query(truncate_hex_data)
print('Truncated Sucessfully')
time.sleep(1)




url = "https://api.helium.io/v1/hotspots/location/box?swlat=35.403115&swlon=-94.424047&nelat=36.479715&nelon=-93.363866"
payload={}
headers = {'User-Agent': 'a1projects/1.0'}
visited_hex = set()
response = request_function(url, headers=headers).json()
for item in response['data']:
    hex = item['location_hex']
    if hex in visited_hex:
        continue
    else:
        visited_hex.add(hex)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args = (hex, dt.datetime.now())
        run_query(insert_hex_data, args)
cursor = response['cursor']

list_of_coordinates = []

############Right here you can save the dat from the previous request to a list or something#####################

while True:
    url = f"https://api.helium.io/v1/hotspots/location/box?swlat=35.403115&swlon=-94.424047&nelat=36.479715&nelon=-93.363866&cursor={cursor}"
    response = request_function(url, headers=headers).json()
    for item in response['data']:
        # print(f"{item['name']}, {item['lng']}, {item['lat']}")
        hex = item['location_hex']
        print(f"{hex}")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hex = item['location_hex']
        print(hex, ' = Cursor Hex')
        args = (hex, dt.datetime.now())
        run_query(insert_hex_data, args)
        print('Finished storing map data')
    cursor = response['cursor']

    # ###########Save data#####################
    if cursor is None:
        break




zohoDB.close()

print("All locations found!!")