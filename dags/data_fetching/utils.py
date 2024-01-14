import boto3
import requests
import pandas as pd

from pandas import DataFrame
from io import BytesIO
from data_fetching.constants import API_KEY_OPENWEATHERMAP, DEFAULT_BUCKET
from data_fetching.air_pollution_api import is_air_quality_alert
from data_fetching.constants import AIR_ALARM, WEATHER_ALARM, API_URL_WEATHER, API_URL_POLLUTION, LOCATION_LON, \
    LOCATION_LAT, USERNAME
from data_fetching.weather_api import to_weather_alert
from data_fetching.model import AirAlerts, WeatherAlerts

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


def read_from_s3(
    bucket,
    key,
    region_name=None,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    aws_session_token=None,
) -> DataFrame:
    client = boto3.client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
    )
    return client.get_object(Bucket=bucket, Key=key)

def request_to_openweathermap(url: str, location_lat, location_lon):
    r = requests.get(url, params={"lat": location_lat, "lon": location_lon, "appid": API_KEY_OPENWEATHERMAP, 'cnt':'8'})
    if r.status_code != 200:
        raise Exception(f"Error on a call to {url} for location {location_lat, location_lon}. HTTP status code: {r.status_code}. Response: {r.json()}")
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


def write_df_to_s3(df, filename, bucket=DEFAULT_BUCKET, **kwargs):
    csv_string = df.to_csv(index=False)
    save_to_s3(bucket=bucket, data=csv_string, key=filename, **kwargs)

def read_df_from_s3(filename, bucket=DEFAULT_BUCKET, **kwargs):
    response = read_from_s3(bucket=bucket, key=filename)
    data = response['Body'].read()
    return pd.read_csv(BytesIO(data))

def print_alerts(weather_alerts, air_alerts):
    weather_alerts[AIR_ALARM] = air_alerts[AIR_ALARM]
    alarms = weather_alerts
    alarms_repr = alarms.to_string(index=False, justify='center')
    print(alarms_repr)


def get_alerts(locations: DataFrame, type_: str) -> DataFrame:
    if type_ == AIR_ALARM:
        api = API_URL_POLLUTION
        func = is_air_quality_alert
    elif type_ == WEATHER_ALARM:
        api = API_URL_WEATHER
        func = to_weather_alert
    else:
        raise ValueError(type_)
    alarms = []
    for _, row in locations.iterrows():
        r = request_to_openweathermap(api, row[LOCATION_LAT], row[LOCATION_LON])
        if r.status_code == 200:
            new_row = [row[USERNAME], func(r)]
            alarms.append(new_row)
    alarms = DataFrame(alarms, columns=[USERNAME, type_])
    return alarms
