from datetime import date, datetime, timedelta, timezone
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import requests
import tweepy
from PIL import Image
import os
import ssl
from io import BytesIO
from PIL import Image
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter
import re
import glob
import matplotlib.ticker as ticker

#Local Time
datetime_object = datetime.now()
today = date.today()

# Yesterday date
yesterday = today - timedelta(days = 2)


helium = 'https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS&resolution=raw&timeframe_start='+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'
ttn  = 'https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS&resolution=raw&timeframe_start='+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'

#RCB Weather Station Mycelium Labs 0auth Keys
consumer_key = "" #api key
consumer_secret = "" #api password
key = ""
secret = ""

# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

#Weather Station Datacake Data
r = requests.get('https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS,WIND&resolution=raw&timeframe_start='+str(yesterday)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
data = r.json()
time_format = "%Y-%m-%dT%H:%M:%SZ"

time1 = "Time:",data[-1]['time']
#print(time1)
hum = float(next(v for i in data if (v := i["HUMIDITY"]) is not None))
print('humidity: ', hum)
temp = float(next(v for i in data if (v := i["TEMPERATURE"]) is not None))
TempF = (temp * (9/5)) + 32         #Converts from Celcius
#print(temp)
gas = float(next(v for i in data if (v := i["GAS"]) is not None))
#print(gas)
pressure = float(next(v for i in data if (v := i["PRESSURE"]) is not None))
#print(pressure)
wind = float(next(v for i in data if (v := i["WIND"]) is not None))
#print(wind)

#Soil Sensor Values
r2 = requests.get('https://api.datacake.co/v1/devices/7c0df4d3-efab-4530-8df3-42af1f432cec/historic_data/?fields=SOIL_TEMPERATURE,SOIL_MOISTURE&resolution=raw&timeframe_start='+str(yesterday)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
data2 = r2.json()
time_format2 = "%Y-%m-%dT%H:%M:%SZ"
time2 = "Time:",data[-1]['time']
#print(time2)
soilTemp = float(next(v for i in data2 if (v := i["SOIL_TEMPERATURE"]) is not None))
soilMoisture = float(next(v for i in data2 if (v := i["SOIL_MOISTURE"]) is not None))
#print(f"Humidity: {hum:.4f}% \nTemperature: {temp:.4f} °F \nWind: {wind:.4f} MPH \nGas: {gas:,.4f} hms \nPressure: {pressure:,.4f} KPa \nSoil Moisture: {soilMoisture:.4f}% \nSoil Temperature: {soilTempF:.4f} °F")
#status = f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.0f} °F"
# api.update_status(status)


#Code block to save the image so we can upload to twitter
#Convert a Matplotlib figure to a PIL Image and return it
def fig2img(fig):
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    return {"buffer": buf, "img": img}



#Soil Temperature Graph===================

plt.style.use('dark_background')

# Graph Config
fig = plt.figure()
#fig.patch.set_facecolor('white')

plt.rcParams["figure.figsize"] = [7.50, 5.50]
plt.rcParams["figure.autolayout"] = True
# Soil Temperature Graph===================
#Soil Temperature Exclude none values from data
resTemp = []
for val in data:
    if val['TEMPERATURE'] != None :
        resTemp.append(val)

soiltemp = resTemp[-1]['TEMPERATURE']


resWind = []
for val in data:
    if val['WIND'] != None :
        resWind.append(val)

windData = resWind[-1]['WIND']

#Soil Moisture exclude none values
resMoist = []
for val in data:
    if val['HUMIDITY'] != None :
        resMoist.append(val)

# This gives us our data excluding none values
#print(f"Soil Temperature Data: \n{res}")
soilMoist = resMoist[-1]['HUMIDITY']

print('resMoist :', soilMoist)

# Puts out data into pandas dataframe
training_set_df = pd.DataFrame(resTemp)
moist_set_df = pd.DataFrame(resMoist)
print('Training set Pandas: \n', moist_set_df)


dfTemp = pd.DataFrame(resTemp, columns = ['TEMPERATURE', 'time'])
dfWind = pd.DataFrame(resWind, columns = ['WIND', 'time'])
dfMoist = pd.DataFrame(resMoist, columns = ['HUMIDITY', 'time'])
print('dfMoist: ', dfMoist)
dfTemp_time = dfTemp['time']
dfMoist_time = dfMoist['time']
dfWind_time = dfWind['time']

#print('df2\n', dfTemp)
dfNPTemp = dfTemp.iloc[:,0]
temp_array = dfNPTemp.to_numpy()

dfNPWind = dfWind.iloc[:,0]
wind_array = dfNPWind.to_numpy()

#convert celcius values to fahrenheit in array
soilCel = np.array(temp_array)
# using formula
feh = soilCel


dfNPMoist = dfMoist.iloc[:,0]
moist_array = dfNPMoist.to_numpy()


plot1= fig.add_subplot(221)
plot2= fig.add_subplot(222)
plot3= fig.add_subplot(212)
plot1.plot(dfMoist_time,moist_array,label='Soil Moisture', color='white')
plot1.set_title("Humidity %")
plot2.plot(dfTemp_time,feh,label='Temp Forecast', color='blue')
plot2.set_title("Ambient Temperature °F")
plot3.plot(dfWind_time,wind_array,label='Wind Speeds', color='red')
plot3.set_title("Wind Speeds - MPH")

plt.xticks([0, len(wind_array)/2, len(wind_array)], ["2 days ago","1 day ago","Now"])
plot1.get_xaxis().set_visible(False)   #makes x axis invisible
plot2.get_xaxis().set_visible(False)   #makes x axis invisible
fig.autofmt_xdate()
plt.savefig('temp.png')
plt.show()

#fig = plt.gcf()

# =========================Twitter Bot Handler =========================
# Upload media to Twitter APIv1.1
ret = api.media_upload(filename="temp.png")
# Attach media to tweet
api.update_status(media_ids=[ret.media_id_string], status= "Weather Data (past 48 hours)")
#Displays graph or whatever image you loaded locally (don't use)
#img.show()


