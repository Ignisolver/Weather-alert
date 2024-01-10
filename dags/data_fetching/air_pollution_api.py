import requests


def is_air_quality_alert(response: requests.Response, min_healthy_aqi=3):
    records_limited = response.json()["list"][:24]
    return any(r["main"]["aqi"] > min_healthy_aqi for r in records_limited)
