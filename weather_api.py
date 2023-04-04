import requests
import json


def get_temp(geo_name):
    api_key = "weather api key"
    weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={geo_name}&appid={api_key}&units=metric"

    result = requests.get(weather_api_url)

    result = json.loads(result.text)

    return round(result["main"]["temp"], 2)
