import json
import urllib.request
import urllib.parse

def get_weather():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid = 1118370"
    #yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"tokyo \")"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    return data

if __name__ == '__main__':
    print(get_weather())
