import csv
from datetime import datetime
from io import StringIO

from airflow import DAG
from airflow.decorators import task

from dags.data_fetching.constants import WEATHER_ALARM, AIR_ALARM
from dags.data_fetching.sheets_api import get_user_locations
from dags.data_fetching.utils import write_df_to_s3, read_from_s3, print_alerts, get_alerts

with DAG(
        dag_id="data_fetching_dag",
        start_date=datetime(2023, 1, 10),
        schedule="5 * * * *",  # run every five minutes
):
    @task
    def get_users_task():
        locations = get_user_locations()
        write_df_to_s3(locations, filename="locations.csv")  # TODO fill s3 params

    @task
    def get_weather_alerts_task():
        locations = read_from_s3(filename="locations.csv")  # TODO fill s3 params
        weather_alerts = get_alerts(locations, WEATHER_ALARM)
        write_df_to_s3(weather_alerts, filename="weather_alerts.csv")  # TODO fill s3 params

    @task
    def get_air_pollution_alerts_task():
        locations = read_from_s3(filename="locations.csv")  # TODO fill s3 params
        air_alerts = get_alerts(locations, AIR_ALARM)
        write_df_to_s3(air_alerts, filename="air_alerts.csv")  # TODO fill s3 params

    @task
    def print_alerts_task():
        weather_alerts = read_from_s3(filename="weather_alerts.csv")  # TODO fill s3 params
        air_alerts = read_from_s3(filename="air_alerts.csv")  # TODO fill s3 params
        print_alerts(weather_alerts, air_alerts)

    get_users_task >> [get_air_pollution_alerts_task, get_weather_alerts_task] >> print_alerts_task

