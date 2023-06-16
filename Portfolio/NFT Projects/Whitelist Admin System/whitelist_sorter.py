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

select_wallet_from_db = 'select wallet_address, accessed, discord_id, discord_username, ip_address from nft_wallet_list'
insert_whitelist = "insert into whitelist (wallet_address, discord_id, ip_address, join_date, accessed, discord_username) VALUES(%s, %s, %s, %s, %s, %s)"
truncate_whitelist = "truncate table whitelist"

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




# Truncate Whitelist ###DEPRECATED
run_query(truncate_whitelist)
time.sleep(2)
print('Truncated Table')


wallet_list = []
solana_pattern = re.compile(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$')

get_wallets = run_query(select_wallet_from_db)
for (wallet_address, accessed, discord_id, discord_username, ip_address) in get_wallets:
    if solana_pattern.match(wallet_address):  # check if wallet address follows Solana pattern
        query = f"UPDATE whitelist SET discord_id = (SELECT discord_id FROM nft_wallet_list WHERE wallet_address = '{wallet_address}' ORDER BY accessed DESC LIMIT 1), ip_address = (SELECT ip_address FROM nft_wallet_list WHERE wallet_address = '{wallet_address}' ORDER BY accessed DESC LIMIT 1) WHERE wallet_address = '{wallet_address}'"
        run_query(query)
        wallet_list.append((wallet_address, accessed, discord_id, discord_username, ip_address))


# print(f"Wallet Array: {wallet_list}")
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



for wallet in unique_wallets_list:
    wallet_address, accessed, discord_id, discord_username, ip_address = wallet
    # Replace discord_id with the most recent entry
    query_discord = f"UPDATE whitelist SET discord_id = '{discord_id}' WHERE discord_id = '{discord_id}' AND accessed < '{accessed}'"
    run_query(query_discord)
    # Replace ip_address with the most recent entry
    query_ip = f"UPDATE whitelist SET ip_address = '{ip_address}' WHERE discord_id = '{discord_id}' AND accessed < '{accessed}'"
    # run_query(query_ip)
    # Insert the updated entry into whitelist
    discord_username = discord_username or ""
    args = (wallet_address,discord_id, ip_address, accessed, now, discord_username)
    run_query(insert_whitelist, args)

    update_query = "UPDATE whitelist SET ip_address = %s WHERE wallet_address = %s"
    run_query(update_query, (ip_address, wallet_address))
delete_query = """DELETE w1 FROM whitelist w1
INNER JOIN whitelist w2 ON w1.wallet_address = w2.wallet_address
WHERE w1.id > w2.id;"""
run_query(delete_query)

if len(wallet_list) > 0:
    print('New items added to DB')
else:
    print('No new items added to DB')

print('Pushed items to whitelist')

zohoDB.close()

