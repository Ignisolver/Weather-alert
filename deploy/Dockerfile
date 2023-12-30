FROM apache/airflow:2.7.2

COPY --chmod=777 ../dags/ ${AIRFLOW_HOME}/
RUN pip install -r ${AIRFLOW_HOME}/requirements.txt
