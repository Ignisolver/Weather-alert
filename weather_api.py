import requests

from typing import List, Dict

from constans import HIGH_WIND_SPEED_THRESHOLD, Location, WeatherAlert
from utils import send_request, is_response_correct, get_list_from_response
from credentials import WEATHER_API_KEY

def get_forcecast_url(location: Location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={location.lat}&lon={location.lon}&appid={WEATHER_API_KEY}&cnt=8"
    return url


def get_alert_from_response(response: requests.Response):
    if not is_response_correct(response):
        print("Response Error")
        return WeatherAlert(False, False)
    list_ = get_list_from_response(response)
    wind_alert = detect_strong_wind(list_)
    rain_alert = detect_rain(list_)
    return WeatherAlert(rain_alert, wind_alert)


def detect_rain(list_hours: list):
    for hour_data in list_hours:
        if get_rain_info(hour_data) == "Rain":
            return True
    return False


def detect_strong_wind(list_hours: list):
    for hour_data in list_hours:
        if get_wind_speed(hour_data) > HIGH_WIND_SPEED_THRESHOLD:
            return True
    return False


def get_rain_info(list_el: dict):
    return list_el["weather"][0]['main']


def get_wind_speed(list_el: dict):
    return list_el["wind"]['speed']


def get_alert_for_location(location: Location):
    url = get_forcecast_url(location=location)
    resp = send_request(url)
    alert = get_alert_from_response(resp)
    return alert


def get_weather_alerts_for_locations(locations: List[Location]) -> Dict[Location, WeatherAlert]:
    alerts = {}
    for location in locations:
        alert = get_alert_for_location(location)
        alerts[location] = alert
    return alerts

