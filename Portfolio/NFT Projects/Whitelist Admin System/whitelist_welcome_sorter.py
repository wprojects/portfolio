# import tensorflow as tf
import requests
import json
# import pandas as pd
import tweepy
import ssl
import twitter
import mysql.connector as mysql
import time
import csv
# import read_csv
import time
from collections import Counter
from dotenv import load_dotenv
from pathlib import Path
import os
import datetime as dt
import re


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['db_user']
db_passw = os.environ['db_pass']
db_host = os.environ['db_host']
db_db = os.environ['db_db']

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)

# Querys ---xprize
select_wallet_from_db = 'select wallet_address, accessed, discord_id, discord_username, ip_address from whitelist'
insert_whitelist = "insert into whitelist_compare (wallet_address, discord_id, ip_address, join_date, accessed, discord_username) VALUES(%s, %s, %s, %s, %s, %s)"
insert_whitelist_welcome = "insert into whitelist_welcome (wallet_address, discord_id, ip_address, join_date, accessed, discord_username) VALUES(%s, %s, %s, %s, %s, %s)"
truncate_whitelist = "truncate table whitelist_welcome"

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

run_query(truncate_whitelist)
time.sleep(2)
print('Trucnated Whitelist Welcome Table')


wallet_list = []
solana_pattern = re.compile(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$')
unique_wallets = set(wallet_list)

now = dt.datetime.now()
unique_wallets = {}
unique_entries = {}

for (wallet_address, accessed, discord_id, discord_username, ip_address) in wallet_list:
    if len(wallet_address) < 45 or len(wallet_address) < 55:
        if discord_id not in unique_entries or accessed > unique_entries[discord_id][1]:
            unique_entries[discord_id] = (wallet_address, accessed, discord_id, discord_username, ip_address)

unique_wallets_list = list(unique_entries.values())

now = dt.datetime.now()
cursor = zohoDB.cursor()


response = requests.get('')
if response.status_code == 200:
    data = response.json()
    # recent_data = data[::-1]  # Reverse the order of recent_data

    recent_data = data[:1]
    recent_data.reverse()
    for item in recent_data:
        accessed = item.get('join_date', 'N/A')
    last_whitelist_item = accessed
    print('API:', last_whitelist_item)

if last_whitelist_item and last_whitelist_item != 'N/A':
    # Get the maximum accessed value from whitelist_test
    print('t1:', last_whitelist_item)
    max_accessed = dt.datetime.strptime(last_whitelist_item, '%Y-%m-%d %H:%M:%S')
    print('test:', max_accessed)
    # Grab everything past that entry in whitelist table
    # select_wallet_from_db = "SELECT wallet_address, accessed, join_date, discord_id, discord_username, ip_address FROM whitelist WHERE join_date > %s"
    select_wallet_from_db = "SELECT wallet_address, accessed, join_date, discord_id, discord_username, ip_address FROM whitelist WHERE join_date > %s AND ip_address = ''"
    cursor.execute(select_wallet_from_db, (max_accessed,))
    wallet_list = cursor.fetchall()
    for wallet in wallet_list:
        wallet_address, accessed, join_date, discord_id, discord_username, ip_address = wallet
        print('Join: ', join_date)
        discord_username = discord_username or ""
        args = (wallet_address, discord_id, ip_address, join_date, now, discord_username)
        run_query(insert_whitelist, args)
        run_query(insert_whitelist_welcome, args)


    if len(wallet_list) > 0:
        print('Data posted to DB')
    else:
        print('No new items added to DB')

# Close the cursor and database connection
cursor.close()
zohoDB.close()

