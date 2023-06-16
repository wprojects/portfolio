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
        """
        Create an instance of Logger Class that takes two parameters
        1 -> Level of the log messages to be logged. Can be configured by typing Logger.Levels "." and choose any level from the list displayed.
        2 -> Absolute file path, where messages need to be logged.
        """
        logger = Logger.get_instance(level=Logger.Levels.INFO, file_path='/home/samwins/zoho/sdk_log.log')

        # Create an UserSignature instance that takes user Email as parameter
        user = UserSignature(email='nick@myceliumnetworks.com')

        """
        Configure the environment
        which is of the pattern Domain.Environment
        Available Domains: USDataCenter, EUDataCenter, INDataCenter, CNDataCenter, AUDataCenter
        Available Environments: PRODUCTION(), DEVELOPER(), SANDBOX()
        """
        environment = USDataCenter.PRODUCTION()

        """
        Create a Token instance that takes the following parameters
        1 -> OAuth client id.
        2 -> OAuth client secret.
        3 -> REFRESH/GRANT token.
        4 -> token type.
        5 -> OAuth redirect URL.
        """
        #Production
        token = OAuthToken(client_id='1000.IQ1VI32ANOCSK441R0VXUNPVXHGH2E', client_secret='202ce51c057945d208b300c5e032601517a15b3b37', grant_token='1000.4d7583d8cf9c76547b3ca33b0eef0781.97127f7518ac86d8b08ae0d482791fc3', redirect_url='http://localhost:8000/zoho')
        #Sanbox
        # token = OAuthToken(client_id='1000.IQ1VI32ANOCSK441R0VXUNPVXHGH2E', client_secret='202ce51c057945d208b300c5e032601517a15b3b37', grant_token='1000.a592ef975407667f0b8f42e795967777.18c4753bf911fe5065a8192d1c725393', redirect_url='http://localhost:8000/zoho')

        """
        Create an instance of TokenStore
        1 -> Absolute file path of the file to persist tokens
        """
        store = FileStore(file_path='/home/samwins/zoho/location_automation/tokens/python_sdk_tokens.txt')

        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

        """
        The path containing the absolute directory path (in the key resource_path) to store user-specific files containing information about fields in modules.
        """
        resource_path = '/home/samwins/zoho/location_automation'

        Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=config, resource_path=resource_path, logger=logger)
############## End of Config Code

        #Database Variables
        load_dotenv()
        env_path = Path('.')/'.env'
        load_dotenv(dotenv_path=env_path)

        #Neo DB Variables
        # db_user = os.environ['meme_db_user']
        # db_passw = os.environ['meme_db_pass']
        # db_host = os.environ['meme_db_host']
        # db_db = os.environ['meme_db_db']

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
        cursor.execute("select record_id, lat, lng from zoho_update_location_records")
        for (record_id, lat, lng) in cursor:
                # print('test: ', lat)
            print(f"Record: {record_id}, Lat: {lat}")
            zohoRecord = ZCRMRecord()

            zohoRecord.set_id(int(record_id))
            # zohoRecord.add_key_value('Status', Choice(status))
            zohoRecord.add_key_value('Latitude', float(lat))
            zohoRecord.add_key_value('Longitude', float(lng))

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