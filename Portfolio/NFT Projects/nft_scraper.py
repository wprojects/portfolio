import mysql.connector as mysql
import datetime as dt
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import requests as r
import aiohttp
import backoff
from collections import Counter
import json

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']

@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
    return response


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

#Count Arrays
total_count_array=[] #Collects the total between all
taste_count_array=[]
pfp_count_array=[]
shroomy_count_array=[]

insert_hotspot_record = "insert into nft_holder_data (current_owner, amount_owned, collection_category, accessed) VALUES(%s, %s, %s, %s)"
truncate_table = "truncate table nft_holder_data"



def pfp():
    # headers = {'User-Agent': 'a1projects/1.0'}
    headers = {'User-Agent': 'a1projects/1.0', 'accept': 'application/json', 'token': ''}
    url = "https://pro-api.solscan.io/v1.0/nft/collection/list_nft/ceb1d7870026357ec3b540c6d3140a5231c0056f044eb2d9f354dda433ccb809?page=1"
    response = r.get(url, headers=headers)
    response = response.json()
    data = response['data']
    collectionAddress = []
    nft_address = [nft['nft_address'] for nft in data['list_nfts']]
    nft_name= [nft['nft_name'] for nft in data['list_nfts']]
    nft_attributes= [nft['nft_attributes'] for nft in data['list_nfts']]
    nft_collection_name= [nft['nft_collection_name'] for nft in data['list_nfts']]
    print("NFT Collection Data:") #\nCollection Name: {nft_collection_name}")
    for nft in data['list_nfts']:
        pfp_nft_address = nft['nft_address']
        pfp_nft_name = nft['nft_name']
        pfp_nft_attributes = nft['nft_attributes']
        pfp_pics = pfp_nft_attributes['properties']['files'][0]['uri']
        nft_url = "https://pro-api.solscan.io/v1.0/nft/token/ownership/" + pfp_nft_address
        nft_response = r.get(nft_url, headers=headers)
        nft_response = nft_response.json()
        current_owner = nft_response['data']['current_nft_wallet']
        print(f"NFT Name: {pfp_nft_name} | PFP NFT Address: {pfp_nft_address} | Current Owner: {current_owner} \nImage URL: {pfp_pics}")
        collectionAddress.append(pfp_nft_address)
        total_count_array.append(current_owner) #Append Total Collection
        pfp_count_array.append(current_owner) #Append Local Collection


def shroomy():
    headers = {'User-Agent': 'a1projects/1.0', 'accept': 'application/json', 'token': ''}
    url = "https://pro-api.solscan.io/v1.0/nft/collection/list_nft/6de3375add2abc104d7ffe2aec5bbbf80086de027f4362f35c2e6ee95c48506b?page=1"
    response = r.get(url, headers=headers)
    response = response.json()
    data = response['data']
    collectionAddress = []
    count_array=[]
    nft_address = [nft['nft_address'] for nft in data['list_nfts']]
    nft_name= [nft['nft_name'] for nft in data['list_nfts']]
    nft_attributes= [nft['nft_attributes'] for nft in data['list_nfts']]
    nft_collection_name= [nft['nft_collection_name'] for nft in data['list_nfts']]
    print("NFT Collection Data:") #\nCollection Name: {nft_collection_name}")
    for nft in data['list_nfts']:
        pfp_nft_address = nft['nft_address']
        pfp_nft_name = nft['nft_name']
        pfp_nft_attributes = nft['nft_attributes']
        pfp_pics = pfp_nft_attributes['properties']['files'][0]['uri']
        nft_url = "https://pro-api.solscan.io/v1.0/nft/token/ownership/" + pfp_nft_address
        nft_response = r.get(nft_url, headers=headers)
        nft_response = nft_response.json()
        current_owner = nft_response['data']['current_nft_wallet']
        print(f"NFT Name: {pfp_nft_name} | PFP NFT Address: {pfp_nft_address} | Current Owner: {current_owner} \nImage URL: {pfp_pics}")
        collectionAddress.append(pfp_nft_address)
        total_count_array.append(current_owner) #Append Total Collection
        shroomy_count_array.append(current_owner) #Append Local Collection

def tasteMycelium():
    headers = {'User-Agent': 'a1projects/1.0', 'accept': 'application/json', 'token': ''}
    url = "https://pro-api.solscan.io/v1.0/nft/collection/list_nft/936b48a665319e6248cf0debe688fd2a82c63ecb4c40ad130338054e3522807a?page=1"
    response = r.get(url, headers=headers)
    response = response.json()
    data = response['data']
    collectionAddress = []
    count_array=[]
    nft_address = [nft['nft_address'] for nft in data['list_nfts']]
    nft_name= [nft['nft_name'] for nft in data['list_nfts']]
    nft_attributes= [nft['nft_attributes'] for nft in data['list_nfts']]
    nft_collection_name= [nft['nft_collection_name'] for nft in data['list_nfts']]
    print("NFT Collection Data:") #\nCollection Name: {nft_collection_name}")
    for nft in data['list_nfts']:
        pfp_nft_address = nft['nft_address']
        pfp_nft_name = nft['nft_name']
        pfp_nft_attributes = nft['nft_attributes']
        pfp_pics = pfp_nft_attributes['properties']['files'][0]['uri']
        nft_url = "https://pro-api.solscan.io/v1.0/nft/token/ownership/" + pfp_nft_address
        nft_response = r.get(nft_url, headers=headers)
        nft_response = nft_response.json()
        current_owner = nft_response['data']['current_nft_wallet']
        print(f"NFT Name: {pfp_nft_name} | Address: {pfp_nft_address} | Current Owner: {current_owner} \nImage URL: {pfp_pics}")
        collectionAddress.append(pfp_nft_address)
        total_count_array.append(current_owner) #Append Total Collection
        taste_count_array.append(current_owner) #Append Local Collection


#PFP Collection Count
def pfp_total():
    duplicates = [item for item, count in Counter(pfp_count_array).items() if count > 0]
    data = {}
    for item in duplicates:
        count = pfp_count_array.count(item)
        print(f"{item} owns {count} NFTs in PFP Collection.")
        data[item] = count
        collection_category = 'pfp_mycelium'
        args = (item, count, collection_category, dt.datetime.now())
        run_query(insert_hotspot_record, args)

#Shroomy Collection Count
def shroomy_total():
    duplicates = [item for item, count in Counter(shroomy_count_array).items() if count > 0]
    data = {}
    for item in duplicates:
        count = shroomy_count_array.count(item)
        print(f"{item} owns {count} NFTs in Shroomy Collection.")
        data[item] = count
        collection_category = 'shroomy_mycelium'
        args = (item, count, collection_category, dt.datetime.now())
        run_query(insert_hotspot_record, args)


#Taste Mycelium Collection Count
def taste_total():
    duplicates = [item for item, count in Counter(taste_count_array).items() if count > 0]
    data = {}
    for item in duplicates:
        count = taste_count_array.count(item)
        print(f"{item} owns {count} NFTs in Taste of Mycelium Collection.")
        data[item] = count
        collection_category = 'taste_mycelium'
        args = (item, count, collection_category, dt.datetime.now())
        run_query(insert_hotspot_record, args)

#Total Collection Count
def entire_collection_total():
    duplicates = [item for item, count in Counter(total_count_array).items() if count > 0]
    data = {}
    for item in duplicates:
        count = total_count_array.count(item)
        print(f"{item} owns {count} NFTs in all Mycelium Collections.")
        data[item] = count
        collection_category = 'combined'
        args = (item, count, collection_category, dt.datetime.now())
        run_query(insert_hotspot_record, args)
    with open('data.json', 'w') as f:
        json.dump(data, f)

#Get Data
tasteMycelium()
pfp()
shroomy()
run_query(truncate_table)
time.sleep(2.1)
print('Truncated Table')
#Count Data
pfp_total()
shroomy_total()
taste_total()
entire_collection_total()