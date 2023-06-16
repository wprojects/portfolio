from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json

class Config:

    CLIENTID = ""
    CLIENTSECRET = ""
    REFRESHTOKEN = ""

    ORGID = "";
    WORKSPACEID = "";

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def export_bulk_data(self, ac):
        job_id = ""
        file_path = "/crm_master_record.csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        bulk.export_bulk_data(download_job, file_path)

try:
    obj = sample()
    obj.export_bulk_data(obj.ac);

except Exception as e:
    print(str(e))
