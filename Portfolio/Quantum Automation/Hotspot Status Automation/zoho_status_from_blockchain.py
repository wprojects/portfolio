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

#Neo Database Variables
# db_user = os.environ['meme_db_user']
# db_passw = os.environ['meme_db_pass']
# db_host = os.environ['meme_db_host']
# db_db = os.environ['meme_db_db']

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']

# SQL queries
# Truncate table to populate it with fresh data from API
truncate_zoho_update_hotspot_records = "TRUNCATE TABLE zoho_update_hotspot_records"
get_crm_hotspot_records = "select record_id, status, address, node_category, location_level, node_tag from master_records"
insert_hotspot_record = "insert into zoho_update_hotspot_records (accessed, record_id, address, status, node_category, location_level, node_tag) VALUES(%s, %s, %s, %s, %s, %s, %s)"

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
# 000
@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
        pass
    return response

run_query(truncate_zoho_update_hotspot_records)
print('Truncated Sucessfully')
time.sleep(10)

hotspot_records = run_query(get_crm_hotspot_records)
hotspot_records_count = run_query(get_crm_hotspot_records)

counter = 0
for (record_id, status, address, node_category, location_level, node_tag) in hotspot_records_count:
    if 'Data - WeatherXM' in node_category:
        continue
    if status in ["Online", "Offline"]:
        if "OOR" in node_tag or '5G Cell - Helium' in node_category:
            continue
        else:
            counter += 1

print('Total Hotspots Deployed: ', counter)

db_count = 0
for (record_id, status, address, node_category, location_level, node_tag) in hotspot_records:
    if status in ["Online", "Offline"]:
        if "OOR" in node_tag or '5G Cell - Helium' in node_category or 'Data - WeatherXM' in node_category:
            pass
        else:
            db_count = db_count + 1
            headers = {'User-Agent': 'a1projects/1.0'}
            # address = address.replace("https://app.hotspotty.net/hotspots/", "")
            # address = address.replace("/rewards", "")
            # address = address.replace("/radios", "")
            # address = address.replace("/radi", "")
            url = "https://api.helium.io/v1/hotspots/" + address
            if len(address) < 1:
                continue
            print(url)
            try:
                response = request_function(url, headers)
                response = response.json()
                data = response['data']
            except KeyError:
                print("Hotspot not found, moving on to the next item")
                continue
            status = data['status']['online']
            print(f"Hotspot Status: {status}")
            status = status.capitalize()
            print("DB Count: ", db_count)
            # print("Counter: ", counter)
            args = (dt.datetime.now(), record_id, address, status, node_category, location_level, node_tag)
            run_query(insert_hotspot_record, args)
            if db_count == counter:
                print('Code Breaking')
                break
zohoDB.close()
print('Code Finished')

