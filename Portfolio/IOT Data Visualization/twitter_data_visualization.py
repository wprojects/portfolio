from datetime import date, datetime, timedelta, timezone
import requests
import tweepy
import schedule #Convert time to GMT to Central https://greenwichmeantime.com/time/to/gmt-central/
import time
#Data Visualizer Libraries
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import operator
import itertools

datetime_object = datetime.now()
today = date.today()
print ('Today: ', today)
print('Launching weather sequences...')

#Twitter Bot Auth Keys
consumer_key = '' # api key
consumer_secret = '' # api passw
key = '' # consumer key
secret = '' # consumer password

# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

def dailysummary():
    r = requests.get('https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS,WIND&resolution=raw&timeframe_start='+str(today)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
    print('Helium API Request: ', r)
    data = r.json()
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))
    print(data)
    print("Time:",data[-1]['time'])
    print("Humidity:",data[-1]['HUMIDITY'] )
    print("Temperature:",data[-1]['TEMPERATURE'])
    print("GAS:",data[-1]['GAS'])
    print("PRESSURE:",data[-1]['PRESSURE'])
    print("WIND:",data[-1]['WIND'])
#Weather Station Variables
    time1 = "Time:",data[-1]['time']
    print(time1)
    hum = float(next(v for i in data if (v := i["HUMIDITY"]) is not None))
    print(hum)
    temp = float(next(v for i in data if (v := i["TEMPERATURE"]) is not None))
    print(temp)
    gas = float(next(v for i in data if (v := i["GAS"]) is not None))
    print(gas)
    pressure = float(next(v for i in data if (v := i["PRESSURE"]) is not None))
    print(pressure)
    wind = float(next(v for i in data if (v := i["WIND"]) is not None))
    print(wind)
    tweetData = pd.DataFrame(str(temp['TEMPERATURE']))
    print('Panda: ', tweetData.columns)
#Soil Sensor Values
    r = requests.get('https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=SOIL_TEMPERATURE,SOIL_MOISTURE&resolution=raw&timeframe_start='+str(today)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
    data = r.json()
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))
    print('Data: ', data)
    time1 = "Time:",data[-1]['time']
    print(time1)
    soilTemp = float(next(v for i in data if (v := i["SOIL_TEMPERATURE"]) is not None))
    print('Soil Temperature: ', soilTemp, '°C')
    soilTempF = (soilTemp * (9/5)) + 32         #Converts from Celcius
    print('Soil Temperature: ', soilTempF, '°F')
    soilMoisture = float(next(v for i in data if (v := i["SOIL_MOISTURE"]) is not None))

    print(f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.4f} °F")

    status = f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.0f} °F"
    #api.update_status(status)

dailysummary()
