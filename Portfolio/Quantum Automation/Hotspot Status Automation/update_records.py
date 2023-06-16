import os
from datetime import date, datetime
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector as mysql
import datetime as dt
import json
import re
#Config
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.store import DBStore, FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig

#Update Records
from datetime import date, datetime
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.attachments import Attachment
from zcrmsdk.src.com.zoho.crm.api.tags import Tag
from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.util import Choice, StreamWrapper
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
# class Record(object):
#     @staticmethod
#     def update_record(module_api_name, record_id):
class SDKInitializer(object):
    @staticmethod
    def initialize():

########Start of Config Code
  
        logger = Logger.get_instance(level=Logger.Levels.INFO, file_path='/')

        # Create an UserSignature instance that takes user Email as parameter
        user = UserSignature(email='')
        environment = USDataCenter.PRODUCTION()

        #Production
        token = OAuthToken(client_id='', client_secret='', grant_token='', redirect_url='http://localhost:8000/zoho')
        #Sanbox
        store = FileStore(file_path='/')

        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

    
        resource_path = '/'

        Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=config, resource_path=resource_path, logger=logger)
############## End of Config Code

        #Database Variables
        load_dotenv()
        env_path = Path('.')/'.env'
        load_dotenv(dotenv_path=env_path)

        #CRM DB Variables
        db_user = os.environ['crm_db_user']
        db_passw = os.environ['crm_db_pass']
        db_host = os.environ['crm_db_host']
        db_db = os.environ['crm_db_db']

        chunk_size = 100
        module_api_name = 'Products'
        sanitized_records = []

        record_operations = RecordOperations()
        header_instance = HeaderMap()

        param_instance = ParameterMap()
        param_instance.add(GetRecordsParam.per_page, chunk_size)

        zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
        cursor = zohoDB.cursor()
        cursor.execute("select record_id, status from zoho_update_hotspot_records")
        for (record_id, status) in cursor:
                # print('test: ', lat)
            print(f"Record: {record_id}, Status: {status}")
            zohoRecord = ZCRMRecord()

            zohoRecord.set_id(int(record_id))
            zohoRecord.add_key_value('Status', Choice(status))
            # zohoRecord.add_key_value('Latitude', float(lat))
            # zohoRecord.add_key_value('Longitude', float(lng))

            sanitized_records.append(zohoRecord)

        for i in range(0, len(sanitized_records), chunk_size):
          param_instance.add(GetRecordsParam.page, i)
          request = BodyWrapper()
          request.set_data(sanitized_records[i:i+chunk_size])
          response = record_operations.update_records(module_api_name, request, header_instance)

          if response is not None:
            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()))


        cursor.close()
        zohoDB.close()

SDKInitializer.initialize()