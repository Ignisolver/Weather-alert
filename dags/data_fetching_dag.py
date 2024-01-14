from datetime import datetime

from airflow import DAG
from airflow.decorators import task

from data_fetching.constants import WEATHER_ALARM, AIR_ALARM
from data_fetching.sheets_api import get_user_locations
from data_fetching.utils import write_df_to_s3, read_from_s3, print_alerts, get_alerts

with DAG(
        dag_id="data_fetching_dag",
        start_date=datetime(2023, 1, 10),
        schedule="@daily",
        catchup=False
):
    @task
    def get_users_task():
        locations = get_user_locations()
        write_df_to_s3(locations, filename="locations.csv")

    @task
    def get_weather_alerts_task():
        locations = read_from_s3(filename="locations.csv")
        weather_alerts = get_alerts(locations, WEATHER_ALARM)
        write_df_to_s3(weather_alerts, filename="weather_alerts.csv")

    @task
    def get_air_pollution_alerts_task():
        locations = read_from_s3(filename="locations.csv")
        air_alerts = get_alerts(locations, AIR_ALARM)
        write_df_to_s3(air_alerts, filename="air_alerts.csv")

    @task
    def print_alerts_task():
        weather_alerts = read_from_s3(filename="weather_alerts.csv")
        air_alerts = read_from_s3(filename="air_alerts.csv")
        print_alerts(weather_alerts, air_alerts)

    get_users_task() >> [get_air_pollution_alerts_task(), get_weather_alerts_task()] >> print_alerts_task()

