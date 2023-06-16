import urllib.request
import ssl
import json
import time
import tweepy
import requests
import math
import sys
import decimal
import flag
import requests as r
from dotenv import load_dotenv
from pathlib import Path
import os
ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#RCB Twitter Keys
consumer_key = os.environ['rcb_api_key']
consumer_secret = os.environ['rcb_api_secret']
key = os.environ['rcb_consumer_key']
secret = os.environ['rcb_consumer_secret']


# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)



def challenger_update(last_node):
#Counts Total # Witnesses ever 3 days
    url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/challenges"
    headers = {'User-Agent': 'a1projects/1.0',}
    response = r.get(url, headers=headers)#.json()
    if str(response) == "<Response [200]>":
        time.sleep(.6)
        response = response.json()
        cursor = response["cursor"]
    cursorUrl = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/challenges?cursor=" + cursor
    headers = {'User-Agent': 'a1projects/1.0',}
    response = r.get(cursorUrl, headers=headers)#.json()
    if str(response) == "<Response [200]>":
        time.sleep(.6)
        # print('Next Page')
        response = response.json()
        data = response["data"]
        print(data)
        for x in data:
            if x["challenger"] == "112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn":
                challengednode = x["path"][0]["challengee"]
                print('Challenged Node: ', challengednode)
                if last_node == challengednode:
                    return challengednode
                newUrl = 'https://api.helium.io/v1/hotspots/' + challengednode
                gatewayassets = json.loads(urllib.request.urlopen(newUrl).read())
                node_name = gatewayassets["data"].get("name")
                city = gatewayassets["data"]["geocode"].get("long_city")
                state = gatewayassets["data"]["geocode"].get("long_state")
                long_country = gatewayassets["data"]["geocode"].get("long_country")
                short_country = gatewayassets["data"]["geocode"].get("short_country")
                flags = flag.flag(short_country)
                print(f"I challenge you {node_name} of {city} {state}, {long_country}. Let's hear you beacon!")
                if state == city:
                #    print(f"I challenge you {node_name} of {city}, {long_country}. Let's hear you beacon!")
                    api.update_status(f"I challenge you {node_name} of {city}, {long_country} {flags}. Let's hear you beacon!")
                else:
                #    print(f"I challenge you {node_name} of {city} {state}, {long_country}. Let's hear you beacon!")
                    api.update_status(f"I challenge you {node_name} of {city}, {state}, {long_country} {flags}. Let's hear you beacon!")
                break

                return challengednode
last_node = None
while True:
    last_node = challenger_update(last_node)
    time.sleep(3600)