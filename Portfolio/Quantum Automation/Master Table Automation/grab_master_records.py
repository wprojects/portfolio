from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json
import datetime
import csv

class Config:

    CLIENTID = "1000.IQ1VI32ANOCSK441R0VXUNPVXHGH2E"
    CLIENTSECRET = "202ce51c057945d208b300c5e032601517a15b3b37"
    REFRESHTOKEN = "1000.cc315b4e6df4549c3a0a7464d04f6c23.2286734ff31db7b5a7da8612b4d37562"

    ORGID = "783527588";
    WORKSPACEID = "2578324000000432001";
    VIEWID = "2578324000001352004";


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




