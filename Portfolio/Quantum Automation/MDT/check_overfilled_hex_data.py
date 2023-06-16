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

########################## SQL queries ##########################
#CRM Record Queries
check_hex_overflow = "select hex from hex_data"
#DB Data Pull Queries
#Insert Queries
insert_hex_data = "INSERT INTO overflow_hex (accessed, hex, hex_overflow, hex_count) values (%s, %s, %s, %s)"
#Truncate Queries
truncate_hex_data = "TRUNCATE TABLE overflow_hex"


# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
headers = {'User-Agent': 'a1projects/1.0'}

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

@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
    return response


check_overflow = run_query(check_hex_overflow)

hex_count = 0
for (hex) in check_overflow:
    # hex_count = hex_count + 1
    # hex = str(hex)
    h3 = str(hex).replace("('", "").replace("',)", "")
    url = f"https://api.helium.io/v1/hotspots/hex/{h3}"
    response = request_function(url, headers=headers).json()
    print(url)
    response = response['data']
    hex_amount = len(response)
    if hex_amount == 0:
        hex_overflown = "Empty"

    if 1 <= hex_amount <= 2:
        hex_overflown = "Light"

    if 3 <= hex_amount <= 4:
        hex_overflown = "Medium"

    if 5 <= hex_amount <= 9:
        hex_overflown = "Heavy"

    if hex_amount >= 10:
        hex_overflown = "Oversaturated"

    print(f"Hex Count for {h3}: {hex_amount}")
    args = (dt.datetime.now(), h3, hex_overflown, hex_amount)
    run_query(insert_hex_data, args)

zohoDB.close()

print("Submitted Overflow data to DB")