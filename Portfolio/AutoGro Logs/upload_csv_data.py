import csv
from datetime import date, datetime, timedelta, timezone
import mysql.connector as mysql
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# CRM DB Variables
db_user = os.environ['db_user']
db_passw = os.environ['db_pass']
db_host = os.environ['db_host']
db_db = os.environ['db']

# Globals ---
zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)

data_array = []

#DB Query
db_query = "INSERT INTO autogro_calibration_logs (accessed, saturation_data, rotations, dry_time, dry_target, moisture_status, dry_time_left) VALUES(%s, %s, %s, %s, %s, %s, %s)"

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


with open('log_data.csv', 'r') as file:
    csv_data = csv.reader(file, delimiter=',')
    for row in csv_data:
        # Process each row here
        accessed, saturation_data, rotations, dry_time, dry_target, moisture_status, dry_time_left = row
        cursor = zohoDB.cursor()
        cursor.execute(db_query, row)
        zohoDB.commit()
print('Uploaded to DB')


