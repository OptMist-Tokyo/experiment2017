#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tweepy
import init
import dht11
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin=4)
api = init.api

num = 1
while True:
    result = instance.read()
    num += 1
    if num > 20:
        api.update_status("気温の取得に失敗しました")
        break
    if result.is_valid():
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")
        message = "現在の部屋の気温は" + str(result.temperature) +"°C、湿度は" + str(result.humidity) +"%です" + "\n" + time
        api.update_status(message)
        break
    time.sleep(1)
