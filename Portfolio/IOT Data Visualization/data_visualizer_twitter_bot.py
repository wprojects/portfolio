from datetime import date, datetime, timedelta, timezone
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import requests
import tweepy
from PIL import Image
import os
import ssl

datetime_object = datetime.now()
today = date.today()
print ('Today: ', today)
print('Launching weather sequences...')

helium = 'https://api.datacake.co/v1/devices/****'+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'
ttn  = 'https://api.datacake.co/v1/devices/****'+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'
#print('Helium API Request: ', helium)
#print('TTN API Request: ', ttn)
ssl._create_default_https_context = ssl._create_unverified_context

def twitter_api():
    #Test Bot Auth Keys
    consumer_key = '' # api key
    consumer_secret = '' # api passw
    key = '' # consumer key
    secret = '' # consumer password


    # Authentication with Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    return api


#Helium Weather Station: ecc2979f-01ab-4c08-b78d-2b5077a13bd5
#Helium Soil Sensor: 7c0df4d3-efab-4530-8df3-42af1f432cec


def dailysummary():
    r = requests.get('https://api.datacake.co/v1/devices/***'})
    print('Helium API Request: ', r)
    data = r.json()
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))
    #print(data)
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

#Soil Sensor Values
    r = requests.get('https://api.datacake.co/v1/devices/7****'})
    data = r.json()
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))
    #print('Data: ', data)
    time1 = "Time:",data[-1]['time']
    print(time1)
    soilTemp = float(next(v for i in data if (v := i["SOIL_TEMPERATURE"]) is not None))
    print('Soil Temperature: ', soilTemp, '°C')
    soilTempF = (soilTemp * (9/5)) + 32         #Converts from Celcius
    print('Soil Temperature: ', soilTempF, '°F')
    soilMoisture = float(next(v for i in data if (v := i["SOIL_MOISTURE"]) is not None))

    print(f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.4f} °F")

    status = f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.0f} °F"
   # api.update_status(status)

dailysummary()

x = [1, 2, 3]
y = [1, 4, 9]
plt.plot(x,y)
pltshow = plt.show

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

x = np.arange(-3,3)
plt.plot(x)
fig = plt.gcf()

img = fig2img(fig)
testing = img.show()


def tweet_image(url, message):
    api = twitter_api()
    filename = '/home/twitter_bot_files/temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")

global lastMeme
lastMeme = ''

message = "Testing!"
tweet_image(testing, message)
#api.update_status(testing)
