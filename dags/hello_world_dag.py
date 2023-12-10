from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="hello_world_dag",
    start_date=datetime(2023, 12, 10),
    schedule="5 * * * *", # run every five minutes
):
    @task
    def print_hello_world():
        print('Hello, world!')
    
    print_hello_world()
