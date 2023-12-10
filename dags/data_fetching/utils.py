import requests
from requests import Response

from constans import AirAlerts, WeatherAlerts


def send_request(url: str):
    resp = requests.get(url=url)
    return resp


def is_response_correct(response: Response):
    if response.status_code != 200:
        return False
    return True


def get_list_from_response(response: Response):
    return response.json()["list"]


def create_alerts_tabele(air_alerts: AirAlerts, weather_alerts:WeatherAlerts):
    alerts_tabele = [(
        "LocationLatitude",
        "LocationLongitude",
        "AirAlert",
        "WindAlert",
        "RainAlert",
    )]

    for location, air_alert in air_alerts.items():
        weather_alert = weather_alerts[location]
        location_row = (location.lat, location.lon,
                        air_alert, weather_alert.wind,
                        weather_alert.rain)
        alerts_tabele.append(location_row)
    return alerts_tabele
