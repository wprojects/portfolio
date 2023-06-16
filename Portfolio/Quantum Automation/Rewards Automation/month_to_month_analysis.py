import mysql.connector as mysql
import datetime as dt
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import requests as r
import backoff
from datetime import date, timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector as mysql
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
# truncate_zoho_update_hotspot_records = "TRUNCATE TABLE zoho_update_hotspot_records"
get_crm_hotspot_records = "select record_id, address, status from zoho_crm_hotspot_records"
insert_hotspot_record = "insert into mycelium_rewards (accessed, record_id, address, amount, date, price) VALUES(%s, %s, %s, %s, %s, %s)"

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

#Backoff for Api Requests
@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function(urlPrice, headers):
    responseTotal = r.get(urlTotal, headers)
    if str(responseTotal) != "<Response [200]>":
            raise TypeError("Error raised, not response 200")
    return responseTotal
@backoff.on_exception(backoff.expo, TypeError, max_tries=1000, max_time=1800)
def request_function4(urlPrice, headers):
    responsePrice = r.get(urlPrice, headers)
    if str(responsePrice) != "<Response [200]>":
            raise TypeError("Error raised, not response 200")
    return responsePrice

#Get current Helium Price
headers = {'User-Agent': 'a1projects/1.0'}
urlPrice = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=helium&order=market_cap_desc%2C%20volume_asc%2C%20volume_desc%2C%20&per_page=100&page=1&sparkline=false&price_change_percentage=24h%2C%207d"
responsePrice = request_function4(urlPrice, headers)
responsePrice = responsePrice.json()
price = responsePrice[0]['current_price']
price = f"{price:.2f}"



start_date = date(2022, 3, 1)
start_date_db = start_date.strftime("%Y-%m-%d")
end_date = date(2022, 3, 31)
end_date_db = end_date.strftime("%Y-%m-%d")
# delta = timedelta(days=30)
# while start_date <= end_date:
#     start_date_db = start_date.strftime("%Y-%m-%d")
#     end_date_db = end_date.strftime("%Y-%m-%d")
#     print('start: ',start_date_db)
#     print('end: ', end_date_db)
#     start_date += delta
#     # end_date+= delta

amount = 0
hotspot_records = run_query(get_crm_hotspot_records)
for (record_id,address,status) in hotspot_records:
    daily = "min_time=-1%20day&bucket=day"
    weekly = "min_time=-1%20week&bucket=day"
    # -1%20week&bucket=week"
    monthly = "min_time=-4%20week&bucket=day"
    headers = {'User-Agent': 'a1projects/1.0'}
    urlTotal = f"https://api.helium.io/v1/hotspots/{address}/rewards/sum?min_time={start_date_db}&max_time={end_date_db}"
    print(urlTotal)
    # responseMonthly = r.get(urlMonthly, headers=headers)#.json()
    responseTotal = request_function(urlTotal, headers)
    responseTotal = responseTotal.json()
    dataTotal = responseTotal['data']['total']
    dataTotal = f"{dataTotal}"
    print('Total Rewards: ', dataTotal)
    # dataTotal += amount
    print(dataTotal)

    args = (dt.datetime.now(), record_id, address, dataTotal, end_date_db, price)
    run_query(insert_hotspot_record, args)

zohoDB.close()
