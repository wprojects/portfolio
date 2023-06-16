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
#print("Yesterday was: ", yesterday)

#print ('Today: ', today)

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
#new dasboard
#old dasboard
r = requests.get('https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS,WIND&resolution=raw&timeframe_start='+str(yesterday)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token ceede0ee65580ba31fac7b5342295f738c0bcab0'})
#print('Helium API Request: ', r)
data = r.json()
time_format = "%Y-%m-%dT%H:%M:%SZ"
data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))


time1 = "Time:",data[-1]['time']
#print(time1)
hum = float(next(v for i in data if (v := i["HUMIDITY"]) is not None))
#print(hum)
temp = float(next(v for i in data if (v := i["TEMPERATURE"]) is not None))
#print(temp)
gas = float(next(v for i in data if (v := i["GAS"]) is not None))
#print(gas)
pressure = float(next(v for i in data if (v := i["PRESSURE"]) is not None))
#print(pressure)
wind = float(next(v for i in data if (v := i["WIND"]) is not None))
#print(wind)

#Soil Sensor Values
r2 = requests.get('https://api.datacake.co/v1/devices/portfolio/historic_data/?fields=SOIL_TEMPERATURE,SOIL_MOISTURE&resolution=raw&timeframe_start='+str(yesterday)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token fb2e796d8e1dcad3fef18e2a96532c610d37fbe1'})
data2 = r2.json()
time_format2 = "%Y-%m-%dT%H:%M:%SZ"
#data2 = sorted(data2, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format2))
#print('Data: ', data2)
time2 = "Time:",data[-1]['time']
#print(time2)
soilTemp = float(next(v for i in data2 if (v := i["SOIL_TEMPERATURE"]) is not None))
#print('Soil Temperature: ', soilTemp, '°C')
soilTempF = (soilTemp * (9/5)) + 32         #Converts from Celcius
#print('Soil Temperature: ', soilTempF, '°F')
soilMoisture = float(next(v for i in data2 if (v := i["SOIL_MOISTURE"]) is not None))
print(f"Humidity: {hum:.4f}% \nTemperature: {temp:.4f} °F \nWind: {wind:.4f} MPH \nGas: {gas:,.4f} hms \nPressure: {pressure:,.4f} KPa \nSoil Moisture: {soilMoisture:.4f}% \nSoil Temperature: {soilTempF:.4f} °F")
status = f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.0f} °F"
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
# Graph Config
fig = plt.figure()
#fig.patch.set_facecolor('white')

plt.rcParams["figure.figsize"] = [7.50, 5.50]
plt.rcParams["figure.autolayout"] = True
# Soil Temperature Graph===================
#Soil Temperature Exclude none values from data
resTemp = []
for val in data2:
    if val['SOIL_TEMPERATURE'] != None :
        resTemp.append(val)

# This gives us our data excluding none values
#print(f"Soil Temperature Data: \n{res}")
soiltemp = resTemp[-1]['SOIL_TEMPERATURE']


#Soil Moisture exclude none values
resMoist = []
for val in data2:
    if val['SOIL_MOISTURE'] != None :
        resMoist.append(val)

# This gives us our data excluding none values
#print(f"Soil Temperature Data: \n{res}")
soilMoist = resMoist[-1]['SOIL_MOISTURE']

plt.style.use('dark_background')

# Puts out data into pandas dataframe
training_set_df = pd.DataFrame(resTemp)
moist_set_df = pd.DataFrame(resMoist)
print('Training set Pandas: \n', training_set_df)
dfTemp = pd.DataFrame(resTemp, columns = ['SOIL_TEMPERATURE', 'time'])

dfMoist = pd.DataFrame(resMoist, columns = ['SOIL_MOISTURE', 'time'])

# Last thing to do is resive x values time data to
# match our temp array size
dfTemp_time = dfTemp['time']
dfMoist_time = dfMoist['time']

#print('df2\n', dfTemp)
dfNPTemp = dfTemp.iloc[:,0]
temp_array = dfNPTemp.to_numpy()
#print(f"Celsius {temp_array}")

#convert celcius values to fahrenheit in array
soilCel = np.array(temp_array)
# using formula
feh = (9 * soilCel / 5 + 32)
# printing results
print(f"Fahrenheit {feh}")


dfNPMoist = dfMoist.iloc[:,0]
moist_array = dfNPMoist.to_numpy()

plot1= fig.add_subplot(211)
plot2= fig.add_subplot(212)
plot1.plot(dfMoist_time,moist_array,label='Soil Moisture')
plot1.set_title("Soil Moisture %")
plot2.plot(dfTemp_time,feh,label='Temp Forecast')
plot2.set_title("Soil Temperature °F")

plt.tight_layout()
plot1.get_xaxis().set_visible(False)   #makes x axis invisible
plt.xticks([0, len(feh)/2, len(feh)], ["2 days ago","1 day ago","Now"])

fig.autofmt_xdate()
plt.savefig('temp.png')
plt.show()

# =========================Twitter Bot Handler =========================
# Upload media to Twitter APIv1.1
ret = api.media_upload(filename="temp.png")
# Attach media to tweet
api.update_status(media_ids=[ret.media_id_string], status= "Soil Data (past 48 hours)")

