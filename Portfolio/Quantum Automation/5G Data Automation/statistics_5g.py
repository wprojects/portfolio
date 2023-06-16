import mysql.connector as mysql
import datetime as dt
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import requests as r
import aiohttp
import backoff

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']

# SQL queries
# Truncate table to populate it with fresh data from API
truncate_zoho_update_hotspot_records = "TRUNCATE TABLE zoho_update_hotspot_records"
get_crm_hotspot_records = "select record_id, status, address from zoho_crm_hotspot_records"
insert_hotspot_record = "insert into zoho_update_hotspot_records (accessed, record_id, address, status) VALUES(%s, %s, %s, %s)"

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

@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
    return response

run_query(truncate_zoho_update_hotspot_records)
print('Truncated Sucessfully')
time.sleep(10)

hotspot_records = run_query(get_crm_hotspot_records)

for (record_id, status, address) in hotspot_records:
  if status == "Online" or status == "Offline":
    headers = {'User-Agent': 'a1projects/1.0'}
    url = "https://api.helium.io/v1/hotspots/" + address
    print(url)
    response = request_function(url, headers)
    response = response.json()
    data = response['data']
    status = data['status']['online']
    print(f"Hotspot Status: {status}")
    status = status.capitalize()

    args = (dt.datetime.now(), record_id, address, status)
    # run_query(insert_hotspot_record, args)

zohoDB.close()

