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

    def get_export_job_details(self, ac):
        job_id = ""
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.get_export_job_details(job_id)
        download_job = job_id
        print(result)
        return download_job

try:
    obj = sample()
    obj.get_export_job_details(obj.ac);

except Exception as e:
    print(str(e))

