
import requests

def call_weather_api():
    lat = "43.7766243700837"
    lon = "-79.23182029896637"
    key = "b4a5e5272a6adcb6c12e86fd61981c33"
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