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
truncate_zoho_update_hotspot_records = "TRUNCATE TABLE zoho_update_5g_hotspot_statistics"
get_crm_hotspot_records = "select record_id, address, product_category from zoho_crm_5g_hotspot_records"
insert_hotspot_record = "insert into zoho_update_5g_hotspot_statistics (accessed, record_id, address, multiplier, speed_test, product_category) VALUES(%s, %s, %s, %s, %s, %s)"

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

run_query(truncate_zoho_update_hotspot_records)
print('Truncated Sucessfully')
time.sleep(10)

hotspot_records = run_query(get_crm_hotspot_records)

for (record_id, address, product_category) in hotspot_records:
    headers = {'User-Agent': 'a1projects/1.0'}
    url = "https://explorer-api.helium.com/api/cell/hotspots/" + address + "/avg-speedtest"
    print(url)
    response = r.get(url, headers)
    # print('Response: ', response)
    if str(response) != "<Response [200]>":
        continue
    response = response.json()
    data = response #['data']
    multiplier = data['rewardMultiplier']
    latency = data['latencyAvgMs']
    upload = data['uploadSpeedAvgBps']
    download = data['downloadSpeedAvgBps']
    download = download / 100000
    upload = upload / 100000
    upload = f"{upload:.0f}"
    download = f"{download:.0f}"
    upload = int(upload)
    download = int(download)
    # latency = int(latency)
    # download = 100
    # upload = 11.1
    # print(type(latency))
    # latency = 60
    print(f"Download: {download} Upload:{upload} Latency:{latency}")
    if 30 > download or 1 >= upload >= 0 or latency >= 101:
        speed = "Failed"
        print(speed)
    elif 30 <= download < 50 or 4 >= upload > 2 or 76 <= latency <= 100:
        speed = "Poor"
        print(speed)
    elif 50 <= download < 100 or 5 >= upload < 10 or 51 <= latency <= 76:
        speed = "Degraded"
        print(speed)
    elif 100 <= download and 10 <= upload and 50 >= latency:
        speed = "Acceptable"
        print(speed)

    args = (dt.datetime.now(), record_id, address, multiplier, speed, product_category)
    run_query(insert_hotspot_record, args)

zohoDB.close()

