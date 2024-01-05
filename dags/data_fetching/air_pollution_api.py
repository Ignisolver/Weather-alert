from typing import List

from model import Location, AirAlerts
from constants import API_URL_POLLUTION
from utils import request_to_openweathermap
import requests


def is_air_quality_alert(response: requests.Response, min_healthy_aqi=3):
    records_limited = response.json()["list"][:24]
    return any(r["main"]["aqi"] < min_healthy_aqi for r in records_limited)


def get_air_alerts(locations: List[Location]) -> AirAlerts:
    alerts = {}
    for location in locations:
        r = request_to_openweathermap(API_URL_POLLUTION, location)
        if r.status_code == 200:
            alerts[location] = is_air_quality_alert(r)
    return alerts
