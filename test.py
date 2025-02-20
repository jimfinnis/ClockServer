import requests
import json
import datetime
from key import key

def get_real_data():

    lat=52
    lon=-4

    url = f'http://api.openweathermap.org/data/3.0/onecall?lon={lon}&lat={lat}&exclude=minutely,alerts&appid={key}&units=metric'
    print(url)

    res = requests.get(url)
    return res.json()

def get_fake_data():
    return json.loads(open("test_onecall_data").read())


data = get_fake_data()

def getstr(data,key=None):
    if key is None:
        dat = data["current"]
    else:
        dat = data["hourly"][key]
    temp = dat["temp"]
    feel = dat["feels_like"]
    wind = dat["wind_speed"]
    gust = dat["wind_gust"]
    if key is None:
        rain = 0
    else:
        rain = dat["pop"]
    weather = ":".join(x["description"] for x in dat["weather"])
    t = datetime.datetime.fromtimestamp(dat["dt"])
    tstr = t.strftime("%H:%M")
    print(tstr,temp,feel,wind,gust,weather,rain)

getstr(data)
for x in range(1,10):
    getstr(data,x)
