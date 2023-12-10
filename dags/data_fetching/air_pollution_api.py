from typing import List

from constans import Location, AirAlerts
from utils import send_request, get_list_from_response
from credentials import WEATHER_API_KEY


def get_pullutoin_url(location: Location):
    url = (f"http://api.openweathermap.org/data/2.5/air_pollution/"
           f"forecast?lat={location.lat}&lon={location.lon}&appid={WEATHER_API_KEY}")
    return url


def is_air_quality_ok(list_: List):
    for data in list_[:24]:
        if data["main"]["aqi"] > 3:
            return True
    return False


def get_air_quality_alert(location: Location):
    url = get_pullutoin_url(location)
    response = send_request(url)
    list_ = get_list_from_response(response)
    quality_alert = is_air_quality_ok(list_)
    return quality_alert


def get_air_alerts_for_locations(locations: List[Location]) -> AirAlerts:
    alerts = {}
    for location in locations:
        alert = get_air_quality_alert(location)
        alerts[location] = alert
    return alerts
