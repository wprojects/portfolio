from datetime import date, datetime, timedelta, timezone
import requests
import tweepy
import schedule #Convert time to GMT to Central https://greenwichmeantime.com/time/to/gmt-central/
import time
datetime_object = datetime.now()

today = date.today()

print ('Today: ', today)
print('Launching weather sequences...')

helium = 'https://api.datacake.co/v1/devices/****'+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'
ttn  = 'https://api.datacake.co/v1/devices/****'+str(today)+'T10:39:00Z&timeframe_end='+str(today)+'T10:00:00Z'
#print('Helium API Request: ', helium)
#print('TTN API Request: ', ttn)

#Test Bot Auth Keys
consumer_key = '' # api key
consumer_secret = '' # api passw
key = '' # consumer key
secret = '' # consumer password


# Authentication with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)




def dailysummary():
    r = requests.get('https://api.datacake.co/v1/devices/****'+str(today)+'T00:00:00Z&timeframe_end='+str(today)+'T23:59:59Z', headers={'Authorization': 'Token '})
    print('Helium API Request: ', r)
    data = r.json()
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    data = sorted(data, reverse=True, key=lambda x: datetime.strptime(x['time'], time_format))
    print(data)
    print("Time:",data[-1]['time'])
    print("Humidity:",data[-1]['HUMIDITY'] )
    print("Temperature:",data[-1]['TEMPERATURE'])
    # print("GAS:",data[-1]['GAS'])
    # print("PRESSURE:",data[-1]['PRESSURE'])

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


    status = f"Humidity: {hum:.0f}% \nTemperature: {temp:.0f} °F"
    api.update_status(status)
dailysummary()

# schedule.every().monday.at("00:00").do(dailysummary)
# schedule.every().tuesday.at("00:00").do(dailysummary)
# schedule.every().wednesday.at("00:00").do(dailysummary)
# schedule.every().thursday.at("00:00").do(dailysummary)
# schedule.every().friday.at("00:00").do(dailysummary)
# schedule.every().saturday.at("00:00").do(dailysummary)
# schedule.every().sunday.at("00:00").do(dailysummary)


# schedule.every().monday.at("06:00").do(dailysummary)
# schedule.every().tuesday.at("06:00").do(dailysummary)
# schedule.every().wednesday.at("06:00").do(dailysummary)
# schedule.every().thursday.at("06:00").do(dailysummary)
# schedule.every().friday.at("06:00").do(dailysummary)
# schedule.every().saturday.at("06:00").do(dailysummary)
# schedule.every().sunday.at("06:00").do(dailysummary)


# schedule.every().monday.at("12:00").do(dailysummary)
# schedule.every().tuesday.at("12:00").do(dailysummary)
# schedule.every().wednesday.at("12:00").do(dailysummary)
# schedule.every().thursday.at("12:00").do(dailysummary)
# schedule.every().friday.at("12:00").do(dailysummary)
# schedule.every().saturday.at("12:00").do(dailysummary)
# schedule.every().sunday.at("12:00").do(dailysummary)

# schedule.every().monday.at("18:00").do(dailysummary)
# schedule.every().tuesday.at("18:00").do(dailysummary)
# schedule.every().wednesday.at("18:00").do(dailysummary)
# schedule.every().thursday.at("18:00").do(dailysummary)
# schedule.every().friday.at("18:00").do(dailysummary)
# schedule.every().saturday.at("18:00").do(dailysummary)
# schedule.every().sunday.at("18:00").do(dailysummary)

# while True:
#     schedule.run_pending()
#     time.sleep(51)
