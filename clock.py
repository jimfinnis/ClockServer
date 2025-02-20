#!/usr/bin/env python3

import datetime
import serial
import time

port = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=.1)

time.sleep(5)

prev_weather_update = None
weather_fetches = 0

while True:
    print("Sending")
    now = datetime.datetime.now()
    if not prev_weather_update or now - prev_weather_update > datetime.timedelta(hours=1):
        prev_weather_update=now
        weather_fetches+=1
        print(f"weather fetches: {weather_fetches}")
        
    s = now.strftime(":L*:w*%H:%M*:M*:g*%a %e %b\n")
    print(s)
    port.write(bytes(s,'utf-8'))
    time.sleep(5)


