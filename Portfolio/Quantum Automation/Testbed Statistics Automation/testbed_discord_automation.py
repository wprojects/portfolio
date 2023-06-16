import mysql.connector as mysql
import datetime as dt
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import requests as r
import aiohttp
import backoff
import http.client


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']

########################## SQL queries
#CRM Record Queries
get_crm_5g_hotspot_records = "select record_id, address, status, node_category, location_level, node_tag  from zoho_update_hotspot_records"
get_crm_5g_radio_records = "select record_id from zoho_crm_5g_radio_records"
get_crm_hotspot_records = "select record_id, status, address, location_level from master_records"
get_crm_host_records =  "select record_id, host_name from zoho_crm_host_records"

#DB Data Pull Queries

db_status_records = "select record_id, address, status, node_category, location_level, node_tag from zoho_update_hotspot_records"
db_reward_records = "select record_id, address from zoho_update_hotspot_rewards"
db_location_records = "select record_id, address from zoho_update_location_records"
db_5g_radio_records = "select record_id from zoho_update_5g_radio_records"
db_5g_statistic_records = "select record_id from zoho_update_5g_hotspot_statistics"
db_witness_records = "select record_id from zoho_update_witness_records"
db_witnessed_records = " select record_id from zoho_update_witnessed_records"
# group_by = "SELECT record_id, status FROM master_records WHERE status = 'Online'"
#Insert Records
insert_5g_hotspot_record = "insert into zoho_update_5g_hotspot_records (accessed, record_id, address, status, product_category) VALUES(%s, %s, %s, %s, %s)"

#Truncate Table
truncate_zoho_update_5g_hotspot_records = "TRUNCATE TABLE zoho_update_5g_hotspot_records"


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


##### CRM Record Data
print("CRM DB Record Counts")
print("---------------------")
l1total=0
l3total=0
l4total=0
l5total=0
level1=0
level3=0
level4=0
level5=0
crm_records = run_query(db_status_records)
for (record_id, address, status, node_category, location_level, node_tag) in crm_records:
    if location_level == "Level 1":
        l1total = l1total + 1
    if location_level == "Level 3":
        l3total = l3total + 1
    if location_level == "Level 4":
        l4total = l4total + 1
    if location_level == "Level 5":
        l5total = l5total + 1
    if location_level == "Level 1" and status == "Offline":
        level1 = level1 + 1
    if location_level == "Level 3" and status == "Offline":
        level3 = level3 + 1
    if location_level == "Level 4" and status == "Offline":
        level4 = level4 + 1
    if location_level == "Level 5" and status == "Offline":
        level5 = level5 + 1

l1fr = level1 / l1total
l1fr = l1fr * 100
l1fr= round(l1fr)
l1fr= f"{l1fr}%"

l3fr = level3 / l3total
l3fr = l3fr * 100
l3fr= round(l3fr)
l3fr= f"{l3fr}%"
l4fr=0
if level4 != 0:
    l4fr = level4 / l4total
else:
    pass
l4fr = l4fr * 100
l4fr= round(l4fr)
l4fr= f"{l4fr}%"

l5fr = level5 / l5total
l5fr = l5fr * 100
l5fr= round(l5fr)
l5fr= f"{l5fr}%"

print('L1: ', l1fr)
print('L3: ', l3fr)
print('L4: ', l4fr)
print('L5: ', l5fr)
print('Level 1 Offline: ', level1)
print('Level 3 Offline: ', level3)
print('Level 4 Offline: ', level4)
print('Level 5 Offline: ', level5)
print('Level 1 Total Count: ', l1total)
print('Level 3 Total Count: ', l3total)
print('Level 4 Total Count: ', l4total)
print('Level 5 Total Count: ', l5total)
print('Level 1 Count: ', level1)
print('level 3 Count: ', level3)
print('Level 4 Count: ', level4)
print('Level 5 Count: ', level5)

print("CRM DB Record Count", len(crm_records))
crm_5g_hotspot_records = run_query(get_crm_5g_hotspot_records)
print("CRM 5G Hotspot Record Count", len(crm_5g_hotspot_records))
crm_5g_radio_records = run_query(get_crm_5g_radio_records)
print("CRM 5G Radio Record Count", len(crm_5g_radio_records))
print("==================================================")
print("DB Data Pull Record Counts")
print("--------------------------")

online_count = 0
offline_count = 0
####### Online/Offline Count
hotspot_status_query = run_query(db_status_records)
for (record_id, address, status, node_category, location_level, node_tag) in hotspot_status_query:
    if status == "Online":
        online_count = online_count + 1
    elif status == "Offline":
        offline_count = offline_count + 1
print('Online Count: ', online_count)
print('Offline Count: ', offline_count)

#Get Date
d = dt.datetime.now()
date = d.strftime("%B %d, %Y")
print(date)

#Get Host Record Count
host_record_query = run_query(get_crm_host_records)
host_record_count = len(host_record_query)
print(f"Host Count: {host_record_count}")

#Get 5G Hotspot Count
hotspot_5g_count = run_query(db_status_records)

count_5g = 0
for (record_id, address, status, node_category, location_level, node_tag) in hotspot_5g_count:
    if node_tag in "OOR":
        pass
    if node_category == "5G Miner - Helium":
        count_5g += 1

print(f"5G Hotspot Deployed Count: {count_5g}")
#5G Offline Report
@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
    return response

# Truncate
# run_query(truncate_zoho_update_5g_hotspot_records)
# print('Truncated Sucessfully')
# time.sleep(10)

offline_list_counter= 0
hotspot_5g_records = run_query(get_crm_5g_hotspot_records)
offline_list = []
for (record_id, address, status, node_category, location_level, node_tag) in hotspot_5g_records:
    if node_category == "5G Miner - Helium":
        headers = {'User-Agent': 'a1projects/1.0'}
        url = "https://api.helium.io/v1/hotspots/" + address
        response = request_function(url, headers)
        explorer_url = "https://explorer.helium.com/hotspots/"
        response = response.json()
        data = response['data']
        status = data['status']['online']
        offline_list_counter += 1
        print(f"Hotspot Status: {status} | Count: {offline_list_counter}")
        status = status.capitalize()
        name =  data['name']
        name = f"{name} |"
        name_address = f"[{name}](<https://explorer.helium.com/hotspots/{address}>)"
        daily_ops = f"[Daily Ops](<https://analytics.zoho.com/open-view/example>)"
        args = (dt.datetime.now(), record_id, address, status, node_category)
        run_query(insert_5g_hotspot_record, args)

        if status == "Offline":
            offline_list.append(name_address)

offline_5g_msg = ' '.join(map(str, offline_list))

discord_message = f"{date}\n\nOnline - {online_count}\nOffline - {offline_count}\n\n**Offline by Level:**\nLevel 1 - {level1} ({l1fr})\nLevel 3 - {level3} ({l3fr})\nLevel 4 - {level4} ({l4fr})\nLevel 5 - {level5} ({l5fr})\n\n**5G Miners Deployed Count:** {count_5g}\n\n5G Miners Offline: {offline_5g_msg}\n\n{daily_ops}"
print(discord_message)

#Discord
conn = http.client.HTTPSConnection('')

conn.request("POST", "/", discord_message)
response = conn.getresponse()
print(response.status, response.reason)


zohoDB.close()
