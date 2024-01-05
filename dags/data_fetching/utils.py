import boto3
import requests
from constants import API_KEY_OPENWEATHERMAP
from model import Location, AirAlerts, WeatherAlerts

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


def request_to_openweathermap(url: str, location: Location):
    r = requests.get(url, params={"lat": location.lat, "lon": location.lon, "key": API_KEY_OPENWEATHERMAP})
    if r.status_code != 200:
        print(f"Error on a call to {url} for location {location}. HTTP status code: {r.status_code}. Response: {r.json()}")
    return r


def create_alerts_table(air_alerts: AirAlerts, weather_alerts: WeatherAlerts):
    alerts_table = [(
        "Latitude",
        "Longitude",
        "IsAirAlert",
        "IsWindAlert",
        "IsRainAlert",
    )]

    for location, air_alert in air_alerts.items():
        weather_alert = weather_alerts[location]
        row = (location.lat, location.lon, air_alert, weather_alert.wind, weather_alert.rain)
        alerts_table.append(row)
    return alerts_table
