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

#Database Variables
# db_user = os.environ['meme_db_user']
# db_passw = os.environ['meme_db_pass']
# db_host = os.environ['meme_db_host']
# db_db = os.environ['meme_db_db']

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']
# def db_write():
# SQL queries
# Truncate table to populate it with fresh data from API
update_witnessed_csv = "select record_id, address, witness_list, witness_count, lat, lng, accessed from zoho_update_witnessed_records"
update_witness_csv = "select record_id, address, witness_list, witness_count, lat, lng, accessed from zoho_update_witness_records"
insert_hotspot_record = "insert into zoho_update_witness_records (accessed, record_id, address, witness_list, witness_count) VALUES(%s, %s, %s, %s, %s)"

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)

def witness_query(statement, args = None):
    cursor = zohoDB.cursor()
    cursor.execute(statement, args)

    if "select" == statement.split()[0]:
        result = cursor.fetchall()
        # print(result)
        c = csv.writer(open("witness_analytics.csv","w"))
        c.writerow(['record_id', 'address', 'witness_list', 'witness_count', 'lat', 'lng', 'accessed'])
        for row in result:
            # c.writerow(row)
            # print(row)
                c.writerow(row)
        cursor.close()
        return result


    else:
        zohoDB.commit()
        cursor.close()

def witnessed_query(statement, args = None):
    cursor = zohoDB.cursor()
    cursor.execute(statement, args)

    if "select" == statement.split()[0]:
        result = cursor.fetchall()
        # print(result)
        c = csv.writer(open("witnessed_analytics.csv","w"))
        c.writerow(['record_id', 'address', 'witnessed_list', 'witnessed_count', 'lat', 'lng', 'accessed'])
        for row in result:
            # c.writerow(row)
            # print(row)
                c.writerow(row)
        cursor.close()
        return result


    else:
        zohoDB.commit()
        cursor.close()


witnessed_query(update_witnessed_csv)
print('Writing Witnessed Data to CSV')

witness_query(update_witness_csv)
print("Writing Witness Data to CSV")

zohoDB.close()
# db_write()