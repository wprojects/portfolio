from bs4 import BeautifulSoup
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
import schedule #Convert time to GMT to Central https://greenwichmeantime.com/time/to/gmt-central/
#spring daylight savings it goes from 12 to 11, fall it goes from 11 to 12
from dotenv import load_dotenv
from pathlib import Path
import os
import datetime
# from datetime import strftime
# from datetime import strptime
import pytz
# from time import strptime, strftime
from urllib.request import urlopen

ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

#RCB Twitter Keys
consumer_key = os.environ['rcb_api_key']
consumer_secret = os.environ['rcb_api_secret']
key = os.environ['rcb_consumer_key']
secret = os.environ['rcb_consumer_secret']

#Test Bot Twitter Keys
# consumer_key = os.environ['test_api_key']
# consumer_secret = os.environ['test_api_secret']
# key = os.environ['test_consumer_key']
# secret = os.environ['test_consumer_secret']

# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


def dailyrewards():
#Daily Earnings Report for RCB
     url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/rewards/sum?min_time=-60%20day&bucket=day"
     headers = {'User-Agent': 'a1projects/1.0',}
     request = urllib.request.Request(url, headers=headers)
     response = urllib.request.urlopen(request)
     assets = json.loads(response.read())
     total = assets["data"][0].get("total")
     print(f"It’s good to be the Bird, just bagged another {total:.2f} $HNT for the day.")
     api.update_status(f"It’s good to be the Bird, just bagged another {total:.2f} $HNT for the day.")
schedule.every().monday.at("23:00").do(dailyrewards)
schedule.every().tuesday.at("23:00").do(dailyrewards)
schedule.every().wednesday.at("23:00").do(dailyrewards)
schedule.every().thursday.at("23:00").do(dailyrewards)
schedule.every().friday.at("23:00").do(dailyrewards)
schedule.every().saturday.at("23:00").do(dailyrewards)
schedule.every().sunday.at("23:00").do(dailyrewards)

def totalrewards():
#Total Rewards Code
     url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/rewards/sum?min_time=-10000%20day"
     headers = {'User-Agent': 'a1projects/1.0',}
     request = urllib.request.Request(url, headers=headers)
     response = urllib.request.urlopen(request)
     assets = json.loads(response.read())
     totalrewards = assets["data"].get("total")
     print(f"It's been a long time I've been here on my perch. {totalrewards:,.0f} $HNT long.")
     api.update_status(f"It's been a long time I've been here on my perch. {totalrewards:,.0f} $HNT long.")
schedule.every().sunday.at("01:00").do(totalrewards)

def totalhotspots():
#Total Hotspots Code
     url = "https://api.helium.io/v1/stats"
     headers = {'User-Agent': 'a1projects/1.0',}
     request = urllib.request.Request(url, headers=headers)
     response = urllib.request.urlopen(request)
     assets = json.loads(response.read())
     totalhotspots = assets["data"]["counts"].get("hotspots")
     print(f"Watching the @helium ecosystem grow tickles my feathers. We now have {totalhotspots:,.0f} nodes on the network.")
     api.update_status(f"Watching the @helium ecosystem grow tickles my feathers. We now have {totalhotspots:,.0f} nodes on the network.")
schedule.every().tuesday.at("18:00").do(totalhotspots)

def forecastweatherupdate():
#This gives forcast information on the weather
     url = "http://api.weatherapi.com/v1/forecast.json?key=ada8c6a635df4233b8922253212905&q=72764&days=3&aqi=no&alerts=yes"
     assets = json.loads(urllib.request.urlopen(url).read())
     avg_temp = assets["forecast"]["forecastday"][0]["day"].get("avgtemp_f")
     weather = assets["forecast"]["forecastday"][0]["day"]["condition"].get("text")
     max_wind = assets["forecast"]["forecastday"][0]["day"].get("maxwind_mph")
     forecast = weather.lower()
     chance_of_rain = assets["forecast"]["forecastday"][0]["day"].get("daily_chance_of_rain")
     api.update_status(f"The skies today in Springdale, Arkansas will be {forecast} with an average temperature of {avg_temp:.0f}°, with wind gusts up to {max_wind:.0f}mph and a {chance_of_rain}% chance of precipitation. Have fun and safe flying out there.")
schedule.every().monday.at("11:00").do(forecastweatherupdate)
schedule.every().tuesday.at("11:00").do(forecastweatherupdate)
schedule.every().wednesday.at("11:00").do(forecastweatherupdate)
schedule.every().thursday.at("11:00").do(forecastweatherupdate)
schedule.every().friday.at("11:00").do(forecastweatherupdate)
schedule.every().saturday.at("11:00").do(forecastweatherupdate)
schedule.every().sunday.at("11:00").do(forecastweatherupdate)

#Counts how many cities and countries the Helium network is in
def countries_cities():
     url = "https://api.helium.io/v1/stats"
     headers = {'User-Agent': 'a1projects/1.0',}
     request = urllib.request.Request(url, headers=headers)
     response = urllib.request.urlopen(request)
     assets = json.loads(response.read())
     city = assets["data"]["counts"].get("cities")
     country = assets["data"]["counts"].get("countries")
     #print(f"Helium's network has now reached {country} countries, and {city:,} cities.")
     api.update_status(f"How delightful! We've got nodes, in different country codes: the Helium Network has now reached {city:,} cities across {country} countries.")
schedule.every().tuesday.at("17:00").do(countries_cities)

#Request new features to people for RCB
def feature_requests():
    print("I enjoy live-tweeting my own data—like beacons, witnesses, $HNT production, local sunrises & storms, and overall growth of the @helium network.\n\nWhat other information would you like me to share from my perch? Peck reply and let a Bird know.")
    api.update_status("I enjoy live-tweeting my own data—like beacons, witnesses, $HNT production, local sunrises & storms, and overall growth of the @helium network.\n\nWhat other information would you like me to share from my perch? Peck reply and let a Bird know.")
schedule.every().wednesday.at("19:30").do(feature_requests)

def block_count():
     url = "https://api.helium.io/v1/stats"
     headers = {'User-Agent': 'a1projects/1.0',}
     request = urllib.request.Request(url, headers=headers)
     response = urllib.request.urlopen(request)
     assets = json.loads(response.read())
     block = assets["data"]["counts"].get("blocks")
     print(f"Jolly me! Network growth looks unstoppable as the Helium blockchain has just confirmed block #{block:,}.")
     api.update_status(f"Jolly me! Network growth looks unstoppable as the Helium blockchain has just confirmed block #{block:,}.")
schedule.every().tuesday.at("22:30").do(block_count)
schedule.every().friday.at("22:30").do(block_count)

def dc_burn():
#Counts Total # Witnesses ever 3 days
    url = "https://api.helium.io/v1/dc_burns/stats"
    headers = {'User-Agent': 'a1projects/1.0',}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    assets = json.loads(response.read())
    hnturl = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=helium&order=market_cap_desc%2C%20volume_asc%2C%20volume_desc%2C%20&per_page=100&page=1&sparkline=false&price_change_percentage=24h%2C%207d"
    hntassets = json.loads(urllib.request.urlopen(hnturl).read())
    dc = assets["data"]["last_week"]["total"]
    price = hntassets[0].get("current_price")
    yo = dc/100000
    hntcount = yo/price
    print(f"Burn baby burn! The @helium network burned {dc:,.0f} data credits ({hntcount:,.0f} $HNT) this week.")
    api.update_status(f"Burn baby burn! The @helium network burned {dc:,.0f} data credits ({hntcount:,.0f} $HNT) this week.")
schedule.every().tuesday.at("21:00").do(dc_burn)

lastTweet = ''

def rcb_joke_tweets():
    #resp = requests.get("https://roughchilibird.com/joke-database/")
    resp = requests.get("https://rcb-jokes.glitch.me")
    soup = BeautifulSoup(resp.text)
    contents = []
    rows = soup.find_all('div', class_='container')
    print('NUMBER OF ROWS', len(rows))
    print('THE ROWS', rows)
    for row in rows:
        data_row = row.find_all('div', class_='row')
        for tweet in data_row:
            contents.append(tweet.text.strip())
    print('contents: ',contents)
    random.shuffle(contents)
    if len(contents) > 0:
        tweet = contents.pop()
    else:
        print('NO TWEETS AVAILABLE, ABORTING. Is there an issue with the password?')
        return
    global lastTweet
    print('lastTweet', lastTweet)
    while lastTweet == tweet:
        tweet = contents.pop()
    lastTweet = tweet
    #print('Tweet', tweet)
    if type(tweet) is str:
        api.update_status(tweet)
        print('Tweet:', tweet)
    else:
        print('ALERT, THE TWEET WAS NOT A STRING, Maybe a tweet was repeated verbatim (word for word)')  #Maybe a tweet was repeated verbatim (word for word)
schedule.every().friday.at("16:00").do(rcb_joke_tweets)


def witnessed_callout():
#Calls out a hotspot RCB has witnessed
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
    url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/witnessed"
    headers = {'User-Agent': 'a1projects/1.0',}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    assets = json.loads(response.read())
    try:
        idx = random.randint(0,120)
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
        print(f"Shoutout to my pal {witcall}, I love it when you call from {distance:,.2f} miles away.")
        api.update_status(f"Shoutout to my pal {witcall}, I love it when you call from {distance:,.2f} miles away.")
    except:
        idx = random.randint(0,80)
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
        print(f"Shoutout to my pal {witcall}, I love it when you call from {distance:,.2f} miles away.")
        api.update_status(f"Shoutout to my pal {witcall}, I love it when you call from {distance:,.2f} miles away.")
schedule.every().day.at("20:15").do(witnessed_callout)

def witness_count():
#Counts Total # Witnesses ever 3 days
    url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/witnesses"
    headers = {'User-Agent': 'a1projects/1.0',}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    assets = json.loads(response.read())
    witdata = assets["data"]
    witness_count = len(witdata)
    if witness_count != 0:
        print(f"I hear all, I see all. Shout out to my {witness_count} witnesses.")
        api.update_status(f"I hear all, I see all. Shout out to my {witness_count} witnesses.")
schedule.every().day.at("15:00").do(witness_count)

def witnessed_count():
#Counts Total # Witnesses ever 3 days
    url = "https://api.helium.io/v1/hotspots/112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn/witnessed"
    headers = {'User-Agent': 'a1projects/1.0',}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    assets = json.loads(response.read())
    witdata = assets["data"]
    witnessed_count = len(witdata)
    if witnessed_count != 0:
        print(f"I hear all, I see all. I am a proud witness to {witnessed_count} friends over this land.")
        api.update_status(f"I hear all, I see all. I am a proud witness to {witnessed_count} friends over this land.")
schedule.every().day.at("19:00").do(witnessed_count)

def witness_distance_callout():
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
schedule.every().day.at("16:00").do(witness_distance_callout)

############Sunrise/Sunset####################

#Sunset Code RCB
def timeConversion(s):
   a=''
   if s[-2:] == "AM" :
      if s[:2] == '12':
          a = str('00' + s[2:8])
      else:
          a = s[:-2]
   else:
      if s[:2] == '12':
          a = s[:-2]
      else:
          a = str(int(s[:2]) + 12) + s[2:8]
   return a

# def sunsetupdate():
# #This gives current conditions of the weather
#     url = "http://api.weatherapi.com/v1/astronomy.json?key=ada8c6a635df4233b8922253212905&q=72764&dt"
#     print(url)
#     assets = json.loads(urllib.request.urlopen(url).read())
#     timed = assets["location"].get("localtime")
#     sunset = assets["astronomy"]["astro"].get("sunset")
#     sunset_trigger = timeConversion(assets["astronomy"]["astro"].get("sunset"))
#     datetime_object = datetime.strptime(timed,
# '%Y-%m-%d %H:%M')
#     sunset_conversion = datetime.strptime(sunset_trigger,
# '%H:%M %p')
#     springdaletimefinal = datetime.strftime(datetime_object,
# '%H:%M')
#     sunsetfinal = datetime.strftime(sunset_conversion,
# '%H:%M')
#     #print('Sunset Time:', sunset_trigger)
#     #print('Sunset Local Time: ', sunsetfinal)
#     #print('Local Time: ', springdaletimefinal)
#     if springdaletimefinal == sunsetfinal:
#         print(f"As the sun sets for another day ({sunset} today in Springdale, Arkansas), I stay on my perch.")
#         api.update_status(f"As the sun sets for another day ({sunset} today in Springdale, Arkansas), I stay on my perch.")
# schedule.every(.1).minutes.do(sunsetupdate)

# def sunriseupdate():
# #This gives current conditions of the weather
#     format = "%H:%M"
#     aware_us_central = datetime.now(pytz.timezone('US/Central'))
#     central = aware_us_central.strftime(format)
#     # print('Central Time: ', central)
#     url = "http://api.weatherapi.com/v1/astronomy.json?key=ada8c6a635df4233b8922253212905&q=72764&dt"
#     # print(url)
#     assets = json.loads(urllib.request.urlopen(url).read())
#     timed = assets["location"].get("localtime")
#     sunrise = assets["astronomy"]["astro"].get("sunrise")
#     sunrisetrigger = assets["astronomy"]["astro"].get("sunrise")
#     datetime_object = datetime.strptime(timed,
# '%Y-%m-%d %H:%M')
#     sunriseconversion = datetime.strptime(sunrisetrigger,
# '%H:%M %p')
#     springdaletimefinal = datetime.strftime(datetime_object,
# '%H:%M')
#     sunrisefinal = datetime.strftime(sunriseconversion,
# '%H:%M')
#     # print(central, sunrisefinal)
#     if central == sunrisefinal:
#         print(f"As the sun comes up for another day ({sunrise} today in Springdale, Arkansas), early bird gets the worm. Top of the morning to you.")
#         api.update_status(f"As the sun comes up for another day ({sunrise} today), early bird gets the worm. Top of the morning to you.")
# schedule.every(.1).minutes.do(sunriseupdate)

# Set the city and state for which we want to get weather alerts
city = "Springdale"
state = "Arkansas"

def storm_alert():
    # Use the OpenWeatherMap API to get the current weather for the specified city and state
    api_key = "eeeed7d95c10a7850e4e9f7c9c7aa328"
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}".format(city, state, api_key)
    print(url)
    response = requests.get(url)
    data = response.json()
    weather_status = data['weather'][0]['description']
    print(f"Current Weather Status: {weather_status}")
    # clear ="clear sky"
    thunder = "thunderstorm"
    snow = "snow"
    tornado = "tornado"
    heavy_rain = "heavy intensity rain"
    very_heavy_rain = " very heavy rain"
    rain_snow = "Rain and snow"

    if weather_status.__contains__(thunder):
        api.update_status("Storms are headed this way, but you won’t catch me leaving my perch. Careful out there birds.")
    if weather_status.__contains__(snow):
        api.update_status("Storms are headed this way, but you won’t catch me leaving my perch. Careful out there birds.")
    if weather_status.__contains__(tornado):
        api.update_status("Storms are headed this way, but you won’t catch me leaving my perch. Careful out there birds.")
    if weather_status.__contains__(heavy_rain):
        api.update_status("Storms are headed this way, but you won’t catch me leaving my perch. Careful out there birds.")
    if weather_status.__contains__(very_heavy_rain):
        api.update_status("Storms are headed this way, but you won’t catch me leaving my perch. Careful out there birds.")
    if weather_status.__contains__(rain_snow):
        api.update_status("Storms are headed this way, but you won’t catch me leaving my perch. Careful out there birds.")
schedule.every(350).minutes.do(storm_alert)


while True:
    schedule.run_pending()
    time.sleep(21)