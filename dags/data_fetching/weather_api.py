import requests

from typing import List, Dict

from model import Location, WeatherAlert
from utils import request_to_openweathermap
from constants import API_URL_WEATHER


def to_weather_alert(response: requests.Response, wind_threshold:int=30):
    records = response.json()["list"]
    return WeatherAlert(is_rain_alert=any(r["weather"][0]['main'] == "Rain" for r in records),
                        is_wind_alert=any(r["wind"]['speed'] > wind_threshold for r in records))


def get_weather_alerts(locations: List[Location]) -> Dict[Location, WeatherAlert]:
    alerts = {}
    for location in locations:
        response = request_to_openweathermap(API_URL_WEATHER, location)
        if response.status_code == 200:
            alerts[location] = to_weather_alert(response)
    return alerts
