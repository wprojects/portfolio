from __future__ import with_statement
from AnalyticsClient import AnalyticsClient
import sys
import json


class Config:

  CLIENTID = ""
  CLIENTSECRET = ""
  REFRESHTOKEN = ""

  ORGID = ""
  WORKSPACEID = ""
  VIEWID = ""


class sample:

  ac = AnalyticsClient(Config.CLIENTID, Config.CLIENTSECRET,
                       Config.REFRESHTOKEN)

  def import_data(self, ac):
    import_type = "truncateadd"
    file_type = "csv"
    auto_identify = "true"
    file_path = "/home/zoho/analytics/witness_data/witness_analytics.csv"
    bulk = ac.get_bulk_instance(Config.ORGID, Config.WORKSPACEID)
    result = bulk.import_data(Config.VIEWID, import_type, file_type,
                              auto_identify, file_path)
    print(result)


try:
  obj = sample()
  obj.import_data(obj.ac)

except Exception as e:
  print(str(e))
