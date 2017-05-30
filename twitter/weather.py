#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import urllib.request
import urllib.parse
import datetime 
def get_weather(day,location=0):
    if location==0 :
        num=1118370 #東京
    elif location==1 :
        num=1117817 #名古屋
    else :
        num=29051428 #大阪       
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid = " + str(num)
    #yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"tokyo \")"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read().decode('utf-8')
    data = json.loads(result)

    
    # weather
    #摂氏華氏換算
    high = float(data['query']['results']['channel']['item']['forecast'][day]['high'])
    low = float(data['query']['results']['channel']['item']['forecast'][day]['low'])
    high = (high-32)/1.8
    low = (low-32)/1.8
    high = round(high,1)
    low = round(low,1)
    #日付の変換
    date = datetime.datetime.strptime(data['query']['results']['channel']['item']['forecast'][day]['date'],'%d %b %Y')
    date = date.strftime('%m月%d日')
    message=date+'の' + data['query']['results']['channel']['location']['city'] + 'の天気は'+data['query']['results']['channel']['item']['forecast'][day]['text'] +'\n'+'最高気温は'+str(high)+'℃  '+'最低気温は'+str(low)+'℃  '
    
    return  message

if __name__ == '__main__':
    print(get_weather(0,0))
