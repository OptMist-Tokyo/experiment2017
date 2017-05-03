#!/usr/bin/env python
# -*- coding:utf-8 -*-

import init
import urllib.request
import os
import datetime
import tweepy
from PIL import Image

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.in_reply_to_screen_name == myscreen_name:
            print("replied by " + status.author.screen_name)
            now = datetime.datetime.now()
            time = now.strftime("%H:%M:%S")
            #画像を受け取って白黒にして返す
            if 'media' in status.entities :
                media_url = status.entities['media'][0]['media_url']
                urllib.request.urlretrieve(media_url, 'reply_img.jpg')
                img = Image.open('reply_img.jpg')
                gray_img = img.convert('L')
                gray_img.save('gray_img.jpg')
                message = '@' + status.author.screen_name + " 画像を変換しました\n" + time
                api.update_with_media(filename = "gray_img.jpg", status = message, in_reply_to_screen_id = status.id)
            else:
                #受け取ったリプライをそのまま返す
                message = '@' + status.author.screen_name + " " +status.text.replace('@'+myscreen_name,"") + "\n" + time
                api.update_status(status = message, in_reply_to_status_id = status.id )
    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            print("followed　by {} {}".format(source_user["name"], source_user["screen_name"]))
            #フォロバ(すでにフォローしている人からフォローされてもリプライを送ってしまう)
            if source_user["id"] != myid:
                api.create_friendship(source_user["id"])
                now = datetime.datetime.now()
                time = now.strftime("%H:%M:%S")
                message = '@'+source_user["screen_name"]+" フォローしました\n" + time
                api.update_status(message)



api = init.api
myid = api.me().id
myscreen_name = api.me().screen_name
stream = tweepy.Stream(api.auth, StreamListener(), secure=True)
print("streaming api start")
stream.userstream()
