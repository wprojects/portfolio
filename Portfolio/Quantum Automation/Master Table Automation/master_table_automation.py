from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import csv
import mysql.connector as mysql
import ssl
import time
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#CRM DB Variables
db_user = os.environ['crm_db_user']
db_passw = os.environ['crm_db_pass']
db_host = os.environ['crm_db_host']
db_db = os.environ['crm_db_db']

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)

# Querys ---
insert_to_master_table = 'insert into master_records (location, active, location_level, location_start_date, hardware, hardware_cost, install_date, crm_link, record_id, node_tag, mn_number, node_name, node_category, antenna, multiplier, speed_test, status, status_date, explorer_link, address, rewards_24h, rewards_7d, rewards_30d, hnt_price, lifetime_earnings, node_direction, lat, lng, accessed) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
truncate_master_table = 'truncate master_records'


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
#Truncate Tables
run_query(truncate_master_table)
print('Truncated Master Records Sucessfully')
time.sleep(1)

class Config:

    CLIENTID = "1000.IQ1VI32ANOCSK441R0VXUNPVXHGH2E"
    CLIENTSECRET = "202ce51c057945d208b300c5e032601517a15b3b37"
    REFRESHTOKEN = "1000.cc315b4e6df4549c3a0a7464d04f6c23.2286734ff31db7b5a7da8612b4d37562"

    ORGID = "783527588";
    WORKSPACEID = "2578324000000432001";
    VIEWID = "2578324000001352004";


class grab_records:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def initiate_bulk_export(self, ac):
        response_format = "csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.initiate_bulk_export(Config.VIEWID, response_format)
        job_id = result
        print('Grab Job ID: ', job_id)
        return job_id

try:
    obj = grab_records()
    pass_job_id = obj.initiate_bulk_export(obj.ac);

except Exception as e:
    print(str(e))
time.sleep(10)
class export:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_export_job_details(self, ac):
        job_id = pass_job_id
        print('Export Job ID: ', job_id)
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.get_export_job_details(job_id)
        download_job = job_id
        print(result)
        return download_job
time.sleep(10)

try:
    obj = export()
    download_job = obj.get_export_job_details(obj.ac);

except Exception as e:
    print(str(e))

class download:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def export_bulk_data(self, ac):
        job_id = download_job
        print('Download Job ID: ', job_id)
        file_path = "/home/samwins/zoho/analytics/master_table/crm_master_record.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        bulk.export_bulk_data(job_id, file_path)
time.sleep(5)

try:
    obj = download()
    obj.export_bulk_data(obj.ac);

except Exception as e:
    print(str(e))

print('Successfully Downloaded Master Table')
with open('crm_master_record.csv', 'r') as file:
    csv_data = csv.reader(file)
    first_row = True
    for row in csv_data:
        if first_row:
            first_row = False
            continue
        cursor = zohoDB.cursor()
        # print(row)
        cursor.execute(insert_to_master_table, row)
        zohoDB.commit()
print('Uploaded CSV --> DB')
zohoDB.close()
