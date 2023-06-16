import urllib.request
import ssl
import json
import time
import tweepy
import requests
import math
import sys
import decimal
import random
from geopy.distance import geodesic
from dotenv import load_dotenv
from pathlib import Path
import os
ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# Twitter Keys
consumer_key = os.environ['test_api_key']
consumer_secret = os.environ['test_api_secret']
key = os.environ['test_consumer_key']
secret = os.environ['test_consumer_secret']
# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


def witness_callout():
#Calls out a witness name every 14.5 hours
#Calculate distance between RCB
    rcbUrl = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn"
    headers = {'User-Agent': 'a1projects/1.0',}
    request = urllib.request.Request(rcbUrl, headers=headers)
    response = urllib.request.urlopen(request)
    rcbAssets = json.loads(response.read())
    rcbLng = rcbAssets["data"]["lng"]
    rcbLat = rcbAssets["data"]["lat"]
    rcbLoc = (rcbLat, rcbLng) # (latitude, longitude) don't confuse
    print('RCB Location: ', rcbLoc)
    url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/witnesses"
    headers = {'User-Agent': 'a1projects/1.0',}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    assets = json.loads(response.read())
    try:
        idx = random.randint(0,60)
        witcall = assets["data"][idx]["name"]
        node_lng = assets["data"][idx]["lng"]
        node_lat = assets["data"][idx]["lat"]
        print('LNG: ', node_lng)
        print('LAT: ',node_lat)
        nodeLoc = (node_lat, node_lng) # (latitude, longitude) don't confuse
        #origin = (30.172705, 31.526725)  # (latitude, longitude) don't confuse
        #dist = (30.288281, 31.732326)
        #print(geodesic(origin, dist).meters)  # 23576.805481751613
        #print(geodesic(origin, dist).kilometers)  # 23.576805481751613
        distance = (geodesic(rcbLoc, nodeLoc).miles)  # 14.64994773134371
        print('Distance: ', distance)
        print(f"Shoutout to my pal {witcall}, I know you’ve been hearing my calls from {distance:,.2f} miles away. try")
        api.update_status(f"Shoutout to my pal {witcall}, I know you’ve been hearing my calls from {distance:,.2f} miles away.")
    except:
        idx = random.randint(0,15)
        witcall = assets["data"][idx]["name"]
        node_lng = assets["data"][idx]["lng"]
        node_lat = assets["data"][idx]["lat"]
        print('LNG: ', node_lng)
        print('LAT: ',node_lat)
        nodeLoc = (node_lat, node_lng) # (latitude, longitude) don't confuse
        #origin = (30.172705, 31.526725)  # (latitude, longitude) don't confuse
        #dist = (30.288281, 31.732326)
        #print(geodesic(origin, dist).meters)  # 23576.805481751613
        #print(geodesic(origin, dist).kilometers)  # 23.576805481751613
        distance = (geodesic(rcbLoc, nodeLoc).miles)  # 14.64994773134371
        print('Distance: ', distance)
        print(f"Shoutout to my pal {witcall}, I know you’ve been hearing my calls from {distance:,.2f} miles away. except")
        api.update_status(f"Shoutout to my pal {witcall}, I know you’ve been hearing my calls from {distance:,.2f} miles away.")
witness_callout()