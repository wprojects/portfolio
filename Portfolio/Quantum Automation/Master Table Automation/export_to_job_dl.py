from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json

class Config:

    CLIENTID = "1000.IQ1VI32ANOCSK441R0VXUNPVXHGH2E"
    CLIENTSECRET = "202ce51c057945d208b300c5e032601517a15b3b37"
    REFRESHTOKEN = "1000.cc315b4e6df4549c3a0a7464d04f6c23.2286734ff31db7b5a7da8612b4d37562"

    ORGID = "783527588";
    WORKSPACEID = "2578324000000432001";

class sample:

    ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET, Config.REFRESHTOKEN)

    def get_export_job_details(self, ac):
        job_id = "2578324000001407005"
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

