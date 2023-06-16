from datetime import date, datetime, timedelta, timezone
import requests
import tweepy
#import schedule #Convert time to GMT to Central https://greenwichmeantime.com/time/to/gmt-central/
import time

datetime_object = datetime.now()

today = date.today()

print ('Today: ', today)
print('Launching weather sequences...')

helium = 'https://api.datacake.co/v1/devices/c444cab6-3047-4146-ab6b-6c48b015f8d3/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS,WIND&resolution=raw&timeframe_start='+str(today)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z'
ttn  = 'https://api.datacake.co/v1/devices/f3f0ac77-eb94-40e1-bd03-31a151ec92f5/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS&resolution=raw&timeframe_start='+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'
print('Helium API Request: ', helium)
#print('TTN API Request: ', ttn)

#Twitter Keys
consumer_key = '' # api key
consumer_secret = '' # api passw
key = '' # consumer key
secret = '' # consumer password



# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

#Helium: c444cab6-3047-4146-ab6b-6c48b015f8d3
#TTN: f3f0ac77-eb94-40e1-bd03-31a151ec92f5
def weather_tweet():
    r = requests.get('https://api.datacake.co/v1/devices/c444cab6-3047-4146-ab6b-6c48b015f8d3/historic_data/?fields=TEMPERATURE,HUMIDITY,PRESSURE,GAS,WIND&resolution=raw&timeframe_start='+str(today)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
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
    #time1 = float(next)(i for i in data if i["time"] is not None)
    print(time1)
    #hum = float(data[-1]["HUMIDITY"])
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
    r = requests.get('https://api.datacake.co/v1/devices/7c0df4d3-efab-4530-8df3-42af1f432cec/historic_data/?fields=SOIL_TEMPERATURE,SOIL_MOISTURE&resolution=raw&timeframe_start='+str(today)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
    data = r.json()
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))
    print('Data: ', data)
    time1 = "Time:",data[-1]['time']
    print(time1)
    soilTemp = float(next(v for i in data if (v := i["SOIL_TEMPERATURE"]) is not None))
    #temp = float(soilTemp[data][-1]["SOIL_MOISTURE"])
    #print('test temp: ', temp)
    print('Soil Temperature: ', soilTemp, '°C')
    soilTempF = (soilTemp * (9/5)) + 32         #Converts from Celcius
    print('Soil Temperature: ', soilTempF, '°F')
    soilMoisture = float(next(v for i in data if (v := i["SOIL_MOISTURE"]) is not None))

    print(f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.4f} °F")

    status = f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F \nWind: {wind:.0f} MPH \nGas: {gas:,.0f} hms \nPressure: {pressure:,.0f} KPa \nSoil Moisture: {soilMoisture:.0f}% \nSoil Temperature: {soilTempF:.0f} °F"
    api.update_status(status)


while True:
    weather_tweet()
    time.sleep(14400)
