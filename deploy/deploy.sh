helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow

# TODO build and publish a Docker image with DAGs included
# https://airflow.apache.org/docs/helm-chart/stable/manage-dags-files.html
# then run sth like:
#helm upgrade --install airflow apache-airflow/airflow \
#   --set images.airflow.repository=my-company/airflow \
#   --set images.airflow.tag=8a0da78