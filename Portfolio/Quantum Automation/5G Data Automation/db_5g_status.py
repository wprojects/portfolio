import requests as r
from dotenv import load_dotenv
from pathlib import Path
import datetime as dt
import os
import time
import mysql.connector as mysql

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
    sql = "TRUNCATE TABLE zoho_update_5g_records"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
truncate()
print('Truncated Sucessfully')
time.sleep(10)

#Record ID DB Call
zohoDB2 = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
#for loop to loop through the records, create address and record id variables
zohoCursor2 = zohoDB2.cursor()
zohoCursor2.execute("select record_id from zoho_crm_5g_records")
result2 = zohoCursor2.fetchall()
result2 = result2
# print(f"DB Results: {len(result)}")

#Status DB Call
zohoDB3 = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
#for loop to loop through the records, create address and record id variables
zohoCursor3 = zohoDB2.cursor()
zohoCursor3.execute("select radio_activity from zoho_crm_5g_records")
result3 = zohoCursor3.fetchall()
result3 = result3

#Address DB Call
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
#for loop to loop through the records, create address and record id variables
zohoCursor = zohoDB.cursor()
record_id = ""
zohoCursor.execute("select address from zoho_crm_5g_records")
result = zohoCursor.fetchall()
# for i in range(len(result2)):
counter = 0
print(len(result))
for i, result3[i] in enumerate(result3):
    counter += 1
    if counter > len(result):
        break
    #Status
    link3 = str(result3[i])
    x3 = str(link3).replace("('", "").replace("',)", "")

    link2 = str(result2[i])
    x2 = str(link2).replace("('", "").replace("',)", "")
    print (x2)
     #Addresses
    link = str(result[i])
    x = str(link).replace("('", "").replace("',)", "")
    headers = {'User-Agent': 'a1projects/1.0'}
    url = "https://explorer-api.helium.com/api/cell/hotspots/" + x +"/cells"
    response = r.get(url, headers=headers)#.json()
    if str(response) == "<Response [200]>":
        time.sleep(.6)
        response = response.json()
        test = len(response)
        print(test)
        if len(response) > 0:
            status = True
            if len(response) == 0:
                status = False
                print('Status: Not Active')
            else:
                if len(response) > 0:
                    print('Status: Active')
                    for i in range(len(response)):
                        # print(response[i])
                        data = response[i]
                        timestamp = dt.datetime.fromtimestamp(data['timestamp'])
                        radio = data['cbsdId']
                        radio = radio[-4:]
                        opmode = data['operationMode']
                        print(f"Radio #: {radio} last heartbeat: {timestamp}")
                        now = dt.datetime.now()
                        isActive = (now - timestamp).total_seconds() <= (24*60*60)

                        # if isActive & opmode:
                        if isActive & opmode:
                            print(f"Radio #: {radio} is Online")

                        else:
                            status = False
                            print(f"Radio #: {radio} is Offline")

            # print(status)
            # Use status here to update your DB
            if status == 1:
                status = "Active"
            if status == 0:
                status = "Inactive"
            zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
            zohoCursor = zohoDB.cursor()
            zohoCursor.execute("insert into zoho_update_5g_records (accessed, record_id, address, radio_activity) VALUES(%s, %s, %s, %s)", (dt.datetime.now(), x2, x, status))
            zohoDB.commit()

        # elif len(response) > 0:
        #     print('Status: Active')
        else:
            print('Status: Inactive')
            zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
            zohoCursor = zohoDB.cursor()
            zohoCursor.execute("insert into zoho_update_5g_records (accessed, record_id, address, radio_activity) VALUES(%s, %s, %s, %s)", (dt.datetime.now(), x2, x, "Inactive"))
            zohoDB.commit()
