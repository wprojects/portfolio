from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json


class Config:

  CLIENTID = "1000.IQ1VI32ANOCSK441R0VXUNPVXHGH2E"
  CLIENTSECRET = "202ce51c057945d208b300c5e032601517a15b3b37"
  REFRESHTOKEN = "1000.cc315b4e6df4549c3a0a7464d04f6c23.2286734ff31db7b5a7da8612b4d37562"

  ORGID = "783527588"
  WORKSPACEID = "2578324000000432001"
  VIEWID = "2578324000000699098"


class sample:

  ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET,
                       Config.REFRESHTOKEN)

  def import_data(self, ac):
    import_type = "truncateadd"
    file_type = "csv"
    auto_identify = "true"
    file_path = "/home/samwins/zoho/analytics/witness_data/witness_analytics.csv"
    bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
    result = bulk.import_data(Config.VIEWID, import_type, file_type,
                              auto_identify, file_path)
    print(result)


try:
  obj = sample()
  obj.import_data(obj.ac)

except Exception as e:
  print(str(e))
