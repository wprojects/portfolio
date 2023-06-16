import mysql.connector as mysql
import datetime as dt
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import requests as r
import backoff

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


def truncate():
# Truncate table to populate it with fresh data from API
    mydb = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
    mycursor = mydb.cursor()
    sql = "TRUNCATE TABLE zoho_update_hotspot_rewards"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
truncate()
time.sleep(10)

zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
DBinsert = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
cursor = zohoDB.cursor()
cursorInsert = DBinsert.cursor()
cursor.execute("select record_id, status, address, node_category, location_level, node_tag from master_records")

@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(url, headers):
    response = r.get(url, headers)
    if str(response) != "<Response [200]>":
        raise TypeError("Error raised, not response 200")
    return response


@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function2(urlWeekly, headers):
    responseWeekly = r.get(urlWeekly, headers)
    if str(responseWeekly) != "<Response [200]>":
            raise TypeError("Error raised, not response 200")
    return responseWeekly


@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function3(urlMonthly, headers):
    responseMonthly = r.get(urlMonthly, headers)
    if str(responseMonthly) != "<Response [200]>":
            raise TypeError("Error raised, not response 200")
    return responseMonthly

@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function4(urlPrice, headers):
    responsePrice = r.get(urlPrice, headers)
    if str(responsePrice) != "<Response [200]>":
            raise TypeError("Error raised, not response 200")
    return responsePrice

@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function5(urlPrice, headers):
    responseTotal = r.get(urlTotal, headers)
    if str(responseTotal) != "<Response [200]>":
            raise TypeError("Error raised, not response 200")
    return responseTotal

headers = {'User-Agent': 'a1projects/1.0'}
urlPrice = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=helium&order=market_cap_desc%2C%20volume_asc%2C%20volume_desc%2C%20&per_page=100&page=1&sparkline=false&price_change_percentage=24h%2C%207d"
responsePrice = request_function4(urlPrice, headers)
responsePrice = responsePrice.json()
price = responsePrice[0]['current_price']
price = f"{price:.2f}"

for (record_id, status, address, node_category, location_level, node_tag) in cursor:
    if 'Data - WeatherXM' in node_category:
        pass
    daily = "min_time=-1%20day&bucket=day"
    weekly = "min_time=-1%20week&bucket=day"
    # -1%20week&bucket=week"
    monthly = "min_time=-4%20week&bucket=day"
    headers = {'User-Agent': 'a1projects/1.0'}
    url = "https://api.helium.io/v1/hotspots/" + address +"/rewards/sum?"+daily
    response = request_function(url, headers)
    response = response.json()
    try:
        data = response['data'][0]
        daily_rewards = data['total']
        daily_rewards = f"{daily_rewards:.2f}"
    except KeyError:
        print(f"No data for record {record_id}")
        pass
    # print('Daily Rewards: ', daily_rewards)
    # cursorInsert.execute("insert into zoho_update_hotspot_rewards (accessed, record_id, address, 24h_rewards) VALUES (%s, %s, %s, %s)", (dt.datetime.now(), record_id, address, daily_rewards))

    urlWeekly = "https://api.helium.io/v1/hotspots/" + address +"/rewards/sum?"+weekly
    responseWeekly = request_function2(urlWeekly, headers)
    responseWeekly = responseWeekly.json()
    try:
        dataWeekly = 0
        for i in range(len(responseWeekly['data'])):
            tempWeekly = responseWeekly['data'][i]['total']
            dataWeekly += tempWeekly
    except KeyError:
        print(f"No data for record {record_id}")
        pass
    urlMonthly = "https://api.helium.io/v1/hotspots/" + address +"/rewards/sum?"+monthly
    print('monthly: ', urlMonthly)
    # responseMonthly = r.get(urlMonthly, headers=headers)#.json()
    responseMonthly = request_function(urlMonthly, headers)
    responseMonthly = responseMonthly.json()
    dataMonthly = 0
    try:
        for i in range(len(responseMonthly['data'])):
            temp = responseMonthly['data'][i]['total']
            dataMonthly += temp
    except KeyError:
        print(f"No data for record {record_id}")
        pass
    urlTotal = "https://api.helium.io/v1/hotspots/" + address +"/rewards/sum?min_time=2018-01-01"
    print(urlTotal)
    # print(urlTotal)
    # responseMonthly = r.get(urlMonthly, headers=headers)#.json()
    responseTotal = request_function5(urlTotal, headers)
    responseTotal = responseTotal.json()
    try:
        dataTotal = responseTotal['data']['total']

        dataTotal = f"{dataTotal:.2f}"
        dataMonthly = f"{dataMonthly:.2f}"
        print('Data Monthly: ', dataMonthly)
        dataWeekly = f"{dataWeekly:.2f}"
        print('Total Rewards: ', dataTotal)
    except KeyError:
        print(f"No data for record {record_id}")
        pass
    cursorInsert.execute("insert into zoho_update_hotspot_rewards (accessed, record_id, address, 24h_rewards, 7d_rewards, 30d_rewards, total_rewards, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (dt.datetime.now(), record_id, address, daily_rewards, dataWeekly, dataMonthly, dataTotal, price))
    DBinsert.commit()
cursor.close()
cursorInsert.close()
zohoDB.close()
DBinsert.close()

