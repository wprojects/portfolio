import os
from datetime import date, datetime

from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.store import DBStore, FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api.request_proxy import RequestProxy

#get records imports
from datetime import date, datetime
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.attachments import Attachment
from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord
from zcrmsdk.src.com.zoho.crm.api.tags import Tag
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api.util import Choice, StreamWrapper
import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector as mysql
import datetime as dt
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


def truncate():
    # Truncate table to populate it with fresh data from API
    #CRM DB Variables
    db_user = os.environ['crm_db_user']
    db_passw = os.environ['crm_db_pass']
    db_host = os.environ['crm_db_host']
    db_db = os.environ['crm_db_db']

    mydb = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
    mycursor = mydb.cursor()
    sql = "TRUNCATE TABLE zoho_crm_5g_radio_records"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
truncate()

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
        token = OAuthToken(client_id='', client_secret='', grant_token='', redirect_url='http://localhost:8000/zoho')

        """
        Create an instance of TokenStore
        1 -> Absolute file path of the file to persist tokens
        """
        store = FileStore(file_path='/home/samwins/zoho/5g_statuses/tokens/get_5g_tokens.txt')

        """
        Create an instance of TokenStore
        1 -> DataBase host name. Default value "localhost"
        2 -> DataBase name. Default value "zohooauth"
        3 -> DataBase user name. Default value "root"
        4 -> DataBase password. Default value ""
        5 -> DataBase port number. Default value "3306"
        6 -> DataBase table name. Default value "oauthtoken" ---> table_name = "oauthtoken"
        """
        # db_user = os.environ['meme_db_user']
        # db_passw = os.environ['meme_db_pass']
        # db_host = os.environ['meme_db_host']
        # db_db = os.environ['meme_db_db']

        # zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
        # #for loop to loop through the records, create address and record id variables
        # zohoCursor = zohoDB.cursor()
        # hotspot_address = ""
        # record_id = ""
        # zohoCursor.execute("insert into zoho_get_hotspot_records (accessed, address, record_id) VALUES(%s, %s, %s)", (dt.datetime.now(), hotspot_address, record_id))
        # zohoDB.commit()
        # zohoCursor.close()
        # zohoDB.close()


        # store = DBStore()
        # store = DBStore(host=db_host, database_name=db_db, user_name=db_user, password=db_passw,port_number='3306')
        # store = DBStore(host="localhost", database_name="zohooauth", user_name="root", password="", port_number="3306")

        """
        auto_refresh_fields
            if True - all the modules' fields will be auto-refreshed in the background, every hour.
            if False - the fields will not be auto-refreshed in the background. The user can manually delete the file(s) or refresh the fields using methods from ModuleFieldsHandler(zcrmsdk/src/com/zoho/crm/api/util/module_fields_handler.py)

        pick_list_validation
            A boolean field that validates user input for a pick list field and allows or disallows the addition of a new value to the list.
            if True - the SDK validates the input. If the value does not exist in the pick list, the SDK throws an error.
            if False - the SDK does not validate the input and makes the API request with the user’s input to the pick list
        """
        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

        """
        The path containing the absolute directory path (in the key resource_path) to store user-specific files containing information about fields in modules.
        """
        resource_path = '/home/samwins/zoho'

        """
        Create an instance of RequestProxy class that takes the following parameters
        1 -> Host
        2 -> Port Number
        3 -> User Name. Default value is None
        4 -> Password. Default value is None
        """
        #request_proxy = RequestProxy(host='proxyHost', port=8080)

        #request_proxy = RequestProxy(host='proxyHost', port=8080, user='userName', password='password')

        """
        Call the static initialize method of Initializer class that takes the following arguments
        1 -> UserSignature instance
        2 -> Environment instance
        3 -> Token instance
        4 -> TokenStore instance
        5 -> SDKConfig instance
        6 -> resource_path
        7 -> Logger instance. Default value is None
        8 -> RequestProxy instance. Default value is None
        """
        Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=config, resource_path=resource_path, logger=logger)
############## End of Config Code
#Get all records code

        """
        example
        module_api_name = 'Leads'
        """
        module_api_name = 'Products'

        # Get instance of RecordOperations Class
        record_operations = RecordOperations()

        # Get instance of ParameterMap Class
        param_instance = ParameterMap()

        ids = [5386077000000546073, 5386077000000428989]

        # Possible parameters for Get Records operation
        # param_instance.add(GetRecordsParam.page, 1)

        # record_operations = RecordOperations()

        # Get instance of ParameterMap Class

        header_instance = HeaderMap()
        for i in range(1, 100):
            param_instance = ParameterMap()
            param_instance.add(GetRecordsParam.per_page, 200)
            param_instance.add(GetRecordsParam.page, i)
            response = record_operations.get_records("Leads", param_instance, header_instance)
            if response is not None:

                # Get the status code from response
                # print('Status Code: ' + str(response.get_status_code()))
                response_object = response.get_object()

                if response_object is not None:

                    # Check if expected ResponseWrapper instance is received.
                    if isinstance(response_object, ResponseWrapper):

                        # Get the list of obtained Record instances
                        record_list = response_object.get_data()

                        for record in record_list:
                            # Get the ID of each Record
                            print("Record ID: " + str(record.get_id()))
                            print('Record KeyValues: ')

                            key_values = record.get_key_values()
                            # print('key values: ', key_values)
                            for key_name, value in key_values.items():
                                if isinstance(value, Choice):
                                    print(key_name + " : " + value.get_value())


        # param_instance.add(GetRecordsParam.page, 1)
        # param_instance.add(GetRecordsParam.per_page, 200)
        #param_instance.add(GetRecordsParam.next_page_token, 2)
        # param_instance.add(GetRecordsParam.per_page, 2)


        # param_instance.add(GetRecordsParam.approved, 'both')

        # param_instance.add(GetRecordsParam.converted, 'both')

        # param_instance.add(GetRecordsParam.cvid, '3409643000000087501')

        #for each_id in ids:
          #  param_instance.add(GetRecordsParam.ids, each_id)
        # print(len(each_id), ' : length')
        param_instance.add(GetRecordsParam.uid, '3409643000000302031')


        # field_names = ["Company", "Email"]
        field_names = ['Explorer_Link', 'Radio_Activity', 'Product_Category', 'Product_Name', 'MN_Number', 'Serial_Num', 'Location', 'Manufacturer']

        for field in field_names:
            param_instance.add(GetRecordsParam.fields, field)

        # param_instance.add(GetRecordsParam.sort_by, 'Email')

        # param_instance.add(GetRecordsParam.sort_order, 'desc')

        start_date_time = datetime(2021, 1, 1, 0, 0, 0)

        param_instance.add(GetRecordsParam.startdatetime, start_date_time)

        end_date_time = datetime(2023, 7, 1, 0, 0, 0)

        # param_instance.add(GetRecordsParam.enddatetime, end_date_time)

        # param_instance.add(GetRecordsParam.territory_id, '3409643000000505351')

        # param_instance.add(GetRecordsParam.include_child, "true")

        # Get instance of HeaderMap Class
        header_instance = HeaderMap()

        # Possible headers for Get Records operation
       # header_instance.add(GetRecordsHeader.if_modified_since, datetime.fromisoformat('2020-01-01T00:00:00+05:30'))

        # Call getRecords method that takes ParameterMap Instance, HeaderMap Instance and module_api_name as parameters
        #param_instance.add(GetRecordsParam.per_page,1)
        for i in range(1,100):
            param_instance1 = ParameterMap()
            param_instance1.add(GetRecordsParam.uid, '3409643000000302031')


            # field_names = ["Company", "Email"]
            field_names = ['Explorer_Link', 'Radio_Activity', 'Status', 'Product_Name', 'Product_Category', 'MN_Number', 'Serial_Num', 'Mycelium_Node_Name', 'Location', 'Manufacturer']

            for field in field_names:
                param_instance1.add(GetRecordsParam.fields, field)

            # param_instance.add(GetRecordsParam.sort_by, 'Email')

            # param_instance.add(GetRecordsParam.sort_order, 'desc')

            start_date_time = datetime(2021, 1, 1, 0, 0, 0)

            param_instance1.add(GetRecordsParam.startdatetime, start_date_time)
            header_instance = HeaderMap()
            param_instance1.add(GetRecordsParam.page, i)

            print('Zoho test page' , param_instance1)
            response = record_operations.get_records(module_api_name, param_instance1, header_instance)

            if response is not None:

                # Get the status code from response
                print('Status Code: ' + str(response.get_status_code()))

                if response.get_status_code() in [204, 304]:
                    print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                    return

                # Get object from response
                response_object = response.get_object()

                if response_object is not None:

                    # Check if expected ResponseWrapper instance is received.
                    if isinstance(response_object, ResponseWrapper):

                        # Get the list of obtained Record instances
                        record_list = response_object.get_data()

                        for record in record_list:
                            # Get the ID of each Record
        #get error with this uncommented
                           # print("Record ID: " + record.get_id())

                            # Get the createdBy User instance of each Record
                            created_by = record.get_created_by()

                            # Check if created_by is not None
                            if created_by is not None:
                                # Get the Name of the created_by User
                                print("Record Created By - Name: " + created_by.get_name())

                                # Get the ID of the created_by User
                                print("Record Created By - ID: " + created_by.get_id())

                                # Get the Email of the created_by User
                                print("Record Created By - Email: " + created_by.get_email())

                            # Get the CreatedTime of each Record
                            print("Record CreatedTime: " + str(record.get_created_time()))

                            if record.get_modified_time() is not None:
                                # Get the ModifiedTime of each Record
                                print("Record ModifiedTime: " + str(record.get_modified_time()))

                            # Get the modified_by User instance of each Record
                            modified_by = record.get_modified_by()

                            # Check if modified_by is not None
                            if modified_by is not None:
                                # Get the Name of the modified_by User
                                print("Record Modified By - Name: " + modified_by.get_name())

                                # Get the ID of the modified_by User
                                print("Record Modified By - ID: " + modified_by.get_id())

                                # Get the Email of the modified_by User
                                print("Record Modified By - Email: " + modified_by.get_email())

                            # Get the list of obtained Tag instance of each Record
                            tags = record.get_tag()

                            if tags is not None:
                                for tag in tags:
                                    # Get the Name of each Tag
                                    print("Record Tag Name: " + tag.get_name())

                                    # Get the Id of each Tag
                                    print("Record Tag ID: " + tag.get_id())

                            # To get particular field value
                            print("Record Field Value: " + str(record.get_key_value('Last_Name')))


                            key_values = record.get_key_values()


                            print('Record KeyValues from CRM: ')

                            for key_name, value in key_values.items():
                                if isinstance(value, list):

                                    if len(value) > 0:

                                        if isinstance(value[0], FileDetails):
                                            file_details = value

                                            for file_detail in file_details:
                                                # Get the Extn of each FileDetails
                                                print("Record FileDetails Extn: " + file_detail.get_extn())

                                                # Get the IsPreviewAvailable of each FileDetails
                                                print("Record FileDetails IsPreviewAvailable: " + str(file_detail.get_is_preview_available()))

                                                # Get the DownloadUrl of each FileDetails
                                                print("Record FileDetails DownloadUrl: " + file_detail.get_download_url())

                                                # Get the DeleteUrl of each FileDetails
                                                print("Record FileDetails DeleteUrl: " + file_detail.get_delete_url())

                                                # Get the EntityId of each FileDetails
                                                print("Record FileDetails EntityId: " + file_detail.get_entity_id())

                                                # Get the Mode of each FileDetails
                                                print("Record FileDetails Mode: " + file_detail.get_mode())

                                                # Get the OriginalSizeByte of each FileDetails
                                                print("Record FileDetails OriginalSizeByte: " + file_detail.get_original_size_byte())

                                                # Get the PreviewUrl of each FileDetails
                                                print("Record FileDetails PreviewUrl: " + file_detail.get_preview_url())

                                                # Get the FileName of each FileDetails
                                                print("Record FileDetails FileName: " + file_detail.get_file_name())

                                                # Get the FileId of each FileDetails
                                                print("Record FileDetails FileId: " + file_detail.get_file_id())

                                                # Get the AttachmentId of each FileDetails
                                                print("Record FileDetails AttachmentId: " + file_detail.get_attachment_id())

                                                # Get the FileSize of each FileDetails
                                                print("Record FileDetails FileSize: " + file_detail.get_file_size())

                                                # Get the CreatorId of each FileDetails
                                                print("Record FileDetails CreatorId: " + file_detail.get_creator_id())

                                                # Get the LinkDocs of each FileDetails
                                                print("Record FileDetails LinkDocs: " + file_detail.get_link_docs())

                                        elif isinstance(value[0], Reminder):
                                            reminders = value

                                            for reminder in reminders:
                                                # Get the Reminder Period
                                                print("Reminder Period: " + reminder.get_period())

                                                # Get the Reminder Unit
                                                print("Reminder Unit: " + reminder.get_unit())

                                        elif isinstance(value[0], Choice):
                                            choice_list = value

                                            print(key_name)

                                            print('Values')

                                            for choice in choice_list:
                                                print(choice.get_value())

                                        elif isinstance(value[0], Participants):
                                            participants = value

                                            for participant in participants:
                                                print("Record Participants Name: " + participant.get_name())

                                                print("Record Participants Invited: " + str(participant.get_invited()))

                                                print("Record Participants Type: " + participant.get_type())

                                                print("Record Participants Participant: " + participant.get_participant())

                                                print("Record Participants Status: " + participant.get_status())

                                        elif isinstance(value[0], InventoryLineItems):
                                            product_details = value

                                            for product_detail in product_details:
                                                line_item_product = product_detail.get_product()

                                                if line_item_product is not None:
                                                    print("Record ProductDetails LineItemProduct ProductCode: " + str(line_item_product.get_product_code()))

                                                    print("Record ProductDetails LineItemProduct Currency: " + str(line_item_product.get_currency()))

                                                    print("Record ProductDetails LineItemProduct Name: " + str(line_item_product.get_name()))

                                                    print("Record ProductDetails LineItemProduct Id: " + str(line_item_product.get_id()))

                                                print("Record ProductDetails Quantity: " + str(product_detail.get_quantity()))

                                                print("Record ProductDetails Discount: " + str(product_detail.get_discount()))

                                                print("Record ProductDetails TotalAfterDiscount: " + str(product_detail.get_total_after_discount()))

                                                print("Record ProductDetails NetTotal: " + str(product_detail.get_net_total()))

                                                if product_detail.get_book() is not None:
                                                    print("Record ProductDetails Book: " + str(product_detail.get_book()))

                                                print("Record ProductDetails Tax: " + str(product_detail.get_tax()))

                                                print("Record ProductDetails ListPrice: " + str(product_detail.get_list_price()))

                                                print("Record ProductDetails UnitPrice: " + str(product_detail.get_unit_price()))

                                                print("Record ProductDetails QuantityInStock: " + str(product_detail.get_quantity_in_stock()))

                                                print("Record ProductDetails Total: " + str(product_detail.get_total()))

                                                print("Record ProductDetails ID: " + str(product_detail.get_id()))

                                                print("Record ProductDetails ProductDescription: " + str(product_detail.get_product_description()))

                                                line_taxes = product_detail.get_line_tax()

                                                for line_tax in line_taxes:
                                                    print("Record ProductDetails LineTax Percentage: " + str(line_tax.get_percentage()))

                                                    print("Record ProductDetails LineTax Name: " + line_tax.get_name())

                                                    print("Record ProductDetails LineTax Id: " + str(line_tax.get_id()))

                                                    print("Record ProductDetails LineTax Value: " + str(line_tax.get_value()))

                                        elif isinstance(value[0], Tag):
                                            tags = value

                                            if tags is not None:
                                                for tag in tags:
                                                    print("Record Tag Name: " + tag.get_name())

                                                    print("Record Tag ID: " + tag.get_id())

                                        elif isinstance(value[0], PricingDetails):
                                            pricing_details = value

                                            for pricing_detail in pricing_details:
                                                print("Record PricingDetails ToRange: " + str(pricing_detail.get_to_range()))

                                                print("Record PricingDetails Discount: " + str(pricing_detail.get_discount()))

                                                print("Record PricingDetails ID: " + pricing_detail.get_id())

                                                print("Record PricingDetails FromRange: " + str(pricing_detail.get_from_range()))

                                        elif isinstance(value[0], ZCRMRecord):
                                            record_list = value

                                            for each_record in record_list:
                                                for key, val in each_record.get_key_values().items():
                                                    print(str(key) + " : " + str(val))

                                        elif isinstance(value[0], LineTax):
                                            line_taxes = value

                                            for line_tax in line_taxes:
                                                print("Record LineTax Percentage: " + str(
                                                    line_tax.get_percentage()))

                                                print("Record LineTax Name: " + line_tax.get_name())

                                                print("Record LineTax Id: " + str(line_tax.get_id()))

                                                print("Record LineTax Value: " + str(line_tax.get_value()))

                                        elif isinstance(value[0], Comment):
                                            comments = value

                                            for comment in comments:
                                                print("Comment-ID: " + str(comment.get_id()))

                                                print("Comment-Content: " + str(comment.get_comment_content()))

                                                print("Comment-Commented_By: " + str(comment.get_commented_by()))

                                                print("Comment-Commented Time: " + str(comment.get_commented_time()))

                                        elif isinstance(value[0], Attachment):
                                            attachments = value

                                            for attachment in attachments:
                                                # Get the ID of each attachment
                                                print('Record Attachment ID : ' + str(attachment.get_id()))
                                                # Get the owner User instance of each attachment
                                                owner = attachment.get_owner()

                                                # Check if owner is not None
                                                if owner is not None:
                                                    # Get the Name of the Owner
                                                    print("Record Attachment Owner - Name: " + owner.get_name())

                                                    # Get the ID of the Owner
                                                    print("Record Attachment Owner - ID: " + owner.get_id())

                                                    # Get the Email of the Owner
                                                    print("Record Attachment Owner - Email: " + owner.get_email())

                                                # Get the modified time of each attachment
                                                print("Record Attachment Modified Time: " + str(attachment.get_modified_time()))

                                                # Get the name of the File
                                                print("Record Attachment File Name: " + attachment.get_file_name())

                                                # Get the created time of each attachment
                                                print("Record Attachment Created Time: " + str(attachment.get_created_time()))

                                                # Get the Attachment file size
                                                print("Record Attachment File Size: " + str(attachment.get_size()))

                                                # Get the parentId Record instance of each attachment
                                                parent_id = attachment.get_parent_id()

                                                if parent_id is not None:
                                                    # Get the parent record Name of each attachment
                                                    print(
                                                        "Record Attachment parent record Name: " + parent_id.get_key_value("name"))

                                                    # Get the parent record ID of each attachment
                                                    print("Record Attachment parent record ID: " + parent_id.get_id())

                                                # Check if the attachment is Editable
                                                print("Record Attachment is Editable: " + str(attachment.get_editable()))

                                                # Get the file ID of each attachment
                                                print("Record Attachment File ID: " + str(attachment.get_file_id()))

                                                # Get the type of each attachment
                                                print("Record Attachment File Type: " + str(attachment.get_type()))

                                                # Get the seModule of each attachment
                                                print("Record Attachment seModule: " + str(attachment.get_se_module()))

                                                # Get the modifiedBy User instance of each attachment
                                                modified_by = attachment.get_modified_by()

                                                # Check if modifiedBy is not None
                                                if modified_by is not None:
                                                    # Get the Name of the modifiedBy User
                                                    print("Record Attachment Modified By - Name: " + modified_by.get_name())

                                                    # Get the ID of the modifiedBy User
                                                    print("Record Attachment Modified By - ID: " + modified_by.get_id())

                                                    # Get the Email of the modifiedBy User
                                                    print("Record Attachment Modified By - Email: " + modified_by.get_email())

                                                # Get the state of each attachment
                                                print("Record Attachment State: " + attachment.get_state())

                                                # Get the createdBy User instance of each attachment
                                                created_by = attachment.get_created_by()

                                                # Check if created_by is not None
                                                if created_by is not None:
                                                    # Get the Name of the createdBy User
                                                    print("Record Attachment Created By - Name: " + created_by.get_name())

                                                    # Get the ID of the createdBy User
                                                    print("Record Attachment Created By - ID: " + created_by.get_id())

                                                    # Get the Email of the createdBy User
                                                    print("Record Attachment Created By - Email: " + created_by.get_email())

                                                # Get the linkUrl of each attachment
                                                print("Record Attachment LinkUrl: " + str(attachment.get_link_url()))

                                        else:
                                            print(key_name)

                                            for each_value in value:
                                                print(str(each_value))

                                elif isinstance(value, User):
                                    print("Record " + key_name + " User-ID: " + str(value.get_id()))

                                    print("Record " + key_name + " User-Name: " + value.get_name())

                                    print("Record " + key_name + " User-Email: " + value.get_email())

                                elif isinstance(value, Layout):
                                    print(key_name + " ID: " + str(value.get_id()))

                                    print(key_name + " Name: " + value.get_name())

                                elif isinstance(value, ZCRMRecord):
                                    # print(key_name + " Record ID: " + value.get_id())

                                    print(key_name + " Record Name: " + value.get_key_value('name'))

                                #get status string
                                elif isinstance(value, Choice):
                                    print(key_name + " : " + value.get_value())
                                    if value.get_value() == "5G Cell - Helium":
                                        # if value.get_value() == "Inactive" or value.get_value() == "Active":
                                    # if value.get_value() == "Inactive" and value.get_value() == "5G - Helium" or value.get_value() == "Active" and value.get_value() == "5G - Helium" or value.get_value() == "None" and value.get_value() == "5G - Helium":
                                        string_status = value.get_value()
                                        print('test: ', value.get_value())
                 #Db Info ===========================================

                                        #CRM DB Variables
                                        db_user = os.environ['crm_db_user']
                                        db_passw = os.environ['crm_db_pass']
                                        db_host = os.environ['crm_db_host']
                                        db_db = os.environ['crm_db_db']


                                        #Insert data to MySQL
                                        zohoDB = mysql.connect(host=db_host ,user=db_user, password=db_passw, database=db_db)
                                        #for loop to loop through the records, create address and record id variables
                                        zohoCursor = zohoDB.cursor()
                                        key_values = record.get_key_values()
                                        # print('key test: ', key_values.items())
                                        exp_link = str(key_values["Explorer_Link"])
                                        exp_link = exp_link.replace("https://explorer.helium.com/hotspots/", "")
                                        exp_link = exp_link.replace("https://app.hotspotty.net/hotspots/", "")
                                        exp_link = exp_link.replace("/rewards", "")
                                        exp_link = exp_link.replace("/radios", "")
                                        exp_link = exp_link.replace("/5g-statistics", "")

                                        record_id = key_values["id"]
                                        status = key_values["Status"]
                                        radio_number = key_values["Product_Name"]
                                        serial_number = key_values["Serial_Num"]
                                        status = str(status)
                                        print("status test: ", status)
                                        hotspot_address = exp_link
                                        zohoCursor.execute("insert into zoho_crm_5g_radio_records (accessed, address, record_id, radio_id, radio_activity, product_category, serial_number) VALUES(%s, %s, %s, %s, %s, %s, %s)", (dt.datetime.now(), hotspot_address, record_id, radio_number, string_status, string_status, serial_number))
                                        zohoDB.commit()
                                        zohoCursor.close()
                                        zohoDB.close()

                                elif isinstance(value, RemindAt):
                                    print(key_name + " : " + value.get_alarm())

                                elif isinstance(value, RecurringActivity):
                                    print(key_name)

                                    print("RRULE: " + value.get_rrule())

                                elif isinstance(value, Consent):
                                    print("Record Consent ID: " + str(value.get_id()))

                                    # Get the createdBy User instance of each Record
                                    created_by = value.get_created_by()

                                    # Check if created_by is not None
                                    if created_by is not None:
                                        # Get the Name of the created_by User
                                        print("Record Consent Created By - Name: " + created_by.get_name())

                                        # Get the ID of the created_by User
                                        print("Record Consent Created By - ID: " + created_by.get_id())

                                        # Get the Email of the created_by User
                                        print("Record Consent Created By - Email: " + created_by.get_email())

                                    # Get the CreatedTime of each Record
                                    print("Record Consent CreatedTime: " + str(value.get_created_time()))

                                    if value.get_modified_time() is not None:
                                        # Get the ModifiedTime of each Record
                                        print("Record Consent ModifiedTime: " + str(value.get_modified_time()))

                                    # Get the Owner User instance of the Consent
                                    owner = value.get_owner()

                                    if owner is not None:
                                        # Get the Name of the Owner User
                                        print("Record Consent Created By - Name: " + owner.get_name())

                                        # Get the ID of the Owner User
                                        print("Record Consent Created By - ID: " + owner.get_id())

                                        # Get the Email of the Owner User
                                        print("Record Consent Created By - Email: " + owner.get_email())

                                    print("Record Consent ContactThroughEmail: " + str(value.get_contact_through_email()))

                                    print("Record Consent ContactThroughSocial: " + str(value.get_contact_through_social()))

                                    print("Record Consent ContactThroughSurvey: " + str(value.get_contact_through_survey()))

                                    print("Record Consent ContactThroughPhone: " + str(value.get_contact_through_phone()))

                                    print("Record Consent MailSentTime: " + str(value.get_mail_sent_time()))

                                    print("Record Consent ConsentDate: " + str(value.get_consent_date()))

                                    print("Record Consent ConsentRemarks: " + value.get_consent_remarks())

                                    print("Record Consent ConsentThrough: " + value.get_consent_through())

                                    print("Record Consent DataProcessingBasis: " + value.get_data_processing_basis())

                                    # To get custom values
                                    print("Record Consent Lawful Reason: " + str(value.get_key_value("Lawful_Reason")))

                                elif isinstance(value, dict):
                                    for key, val in value.items():
                                        print(key + " : " + str(val))

                                else:
                                    print(key_name + " : " + str(value))

                        info = response_object.get_info()

                        if info is not None:
                            if info.get_per_page() is not None:
                                # Get the PerPage from Info
                                print('Record Info PerPage: ' + str(info.get_per_page()))

                            if info.get_page() is not None:
                                # Get the Page from Info
                                print('Record Info Page: ' + str(info.get_page()))

                            if info.get_count() is not None:
                                # Get the Count from Info
                                print('Record Info Count: ' + str(info.get_count()))

                            if info.get_more_records() is not None:
                                # Get the MoreRecords from Info
                                print('Record Info MoreRecords: ' + str(info.get_more_records()))

                    # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        # Get the Status
                        print("Status: " + response_object.get_status().get_value())

                        # Get the Code
                        print("Code: " + response_object.get_code().get_value())

                        print("Details")

                        # Get the details dict
                        details = response_object.get_details()

                        for key, value in details.items():
                            print(key + ' : ' + str(value))

                        # Get the Message
                        print("Message: " + response_object.get_message().get_value())


SDKInitializer.initialize()



