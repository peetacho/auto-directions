
import requests

def call_weather_api():
    # lat and lon are the lattitude and longitude values of your location 
    lat = "<ADRESS_LAT>"
    lon = "<ADRESS_LON>"
    key = "<YOUR_API_KEY>"

    units = "metric"
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units={}".format(lat, lon, key, units)

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    w_dict = response.json()
    weather_dict = w_dict['weather'][0]

    icon_link = "http://openweathermap.org/img/wn/{}@2x.png".format(weather_dict['icon'])
    weather_description = weather_dict['description'].capitalize()
    # [weather description, weather icon link, temp, humidity]
    weather_info = [weather_description, icon_link, w_dict['main']['temp'], w_dict['main']['humidity']]

    return weather_info