import requests
import boto3
from requests import Response

from constans import AirAlerts, WeatherAlerts

def save_to_s3(
    bucket,
    key,
    data,
    region_name=None,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    aws_session_token=None,
):
    client = boto3.client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
    )
    client.put_object(
        Body=data,
        Bucket=bucket,
        Key=key,
    )


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
