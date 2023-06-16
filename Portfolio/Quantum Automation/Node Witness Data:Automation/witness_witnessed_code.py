import urllib.request
import ssl
import json
import time
import tweepy
import requests
import math
import sys
import decimal
import requests as r
import aiohttp
import backoff
import mysql.connector as mysql
import datetime as dt
from dotenv import load_dotenv
from pathlib import Path
import os
import csv

ssl._create_default_https_context = ssl._create_unverified_context


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']


# Witness SQL queries
#Truncate Queries
truncate_zoho_witness_records = "TRUNCATE TABLE zoho_update_witness_records"
truncate_zoho_witnessed_records = "TRUNCATE TABLE zoho_update_witnessed_records"

get_witness_records = "select record_id, status, address, node_category, location_level, node_tag from master_records"
insert_witness_record = "insert into zoho_update_witness_records (accessed, record_id, address, witness_list, witness_count, lat, lng) VALUES(%s, %s, %s, %s, %s, %s, %s)"

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

#Truncate Tables
run_query(truncate_zoho_witness_records)
print('Truncated Witness Records Sucessfully')
time.sleep(5)
run_query(truncate_zoho_witnessed_records)
print('Truncated Witnessed Records Sucessfully')
time.sleep(5)

print('Populating Witness Table')
witness_api_records = run_query(get_witness_records)
for (record_id, status, address, node_category, location_level, node_tag) in witness_api_records:
    if node_category == "5G Miner - Helium" or node_category == "IoT - Helium":
        headers = {'User-Agent': 'a1projects/1.0'}
        url = "https://api.helium.io/v1/hotspots/" + address + "/witnesses"
        response = request_function(url, headers)
        print(url)
        assets = response.json()
        witdata = assets["data"]
        witness_count = len(witdata)
        for i in range(len(witdata)):
            witnesses = assets['data'][i]['name']
            try:
                lat = assets['data'][i]['lat']
                lat = f"{lat:.15}"
            except KeyError:
                lat = None
            try:
                lng = assets['data'][i]['lng']
                lng = f"{lng:.15}"
            except KeyError:
                lng = None
            args = (dt.datetime.now(), record_id, address, witnesses, witness_count, lat, lng)
            run_query(insert_witness_record, args)

zohoDB.close()
print('Witness Table has been populated')


# SQL queries
get_witnessed_records = "select record_id, status, address, node_category, location_level, node_tag from master_records"
insert_witnessed_record = "insert into zoho_update_witnessed_records (accessed, record_id, address, witness_list, witness_count, lat, lng) VALUES(%s, %s, %s, %s, %s, %s, %s)"

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)

def run_witnessed_query(statement, args = None):
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

print('Populating Witnessed Table')
witnessed_records = run_witnessed_query(get_witnessed_records)
for (record_id, status, address, node_category, location_level, node_tag) in witnessed_records:
#   if status == "Online" or status == "Offline":
  if node_category == "5G Miner - Helium" or node_category == "IoT - Helium":
    headers = {'User-Agent': 'a1projects/1.0'}
    url = "https://api.helium.io/v1/hotspots/" + address + "/witnessed"
    response = request_function(url, headers)
    assets = response.json()
    witdata = assets["data"]
    witness_count = len(witdata)
    for i in range(len(witdata)):
        witnesses = assets['data'][i]['name']
        try:
            lat = assets['data'][i]['lat']
            lat = f"{lat:.15}"
        except KeyError:
            lat = None
        try:
            lng = assets['data'][i]['lng']
            lng = f"{lng:.15}"
        except KeyError:
            lng = None
        args = (dt.datetime.now(), record_id, address, witnesses, witness_count, lat, lng)
        run_query(insert_witnessed_record, args)



zohoDB.close()

