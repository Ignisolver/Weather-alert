FROM apache/airflow:2.7.2-python3.11

ADD --chmod=777 dags ${AIRFLOW_HOME}/dags/
RUN pip install -r ${AIRFLOW_HOME}/dags/requirements.txt
