from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json
import datetime
import csv

class Config:

    CLIENTID = ""
    CLIENTSECRET = ""
    REFRESHTOKEN = ""

    ORGID = "";
    WORKSPACEID = "";
    VIEWID = "";


class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def initiate_bulk_export(self, ac):
        response_format = "csv"
        bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
        result = bulk.initiate_bulk_export(Config.VIEWID, response_format)
        job_id = result
        print(result)
        return job_id

try:
    obj = sample()
    obj.initiate_bulk_export(obj.ac);

except Exception as e:
    print(str(e))




