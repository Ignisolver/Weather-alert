import requests


def to_weather_alert(response: requests.Response, wind_threshold: int=30):
    records = response.json()["list"]
    return (any(r["weather"][0]['main'] == "Rain" for r in records) or
            any(r["wind"]['speed'] > wind_threshold for r in records))
