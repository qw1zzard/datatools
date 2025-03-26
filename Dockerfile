FROM apache/airflow:2.10.5

WORKDIR /opt/airflow

COPY dags/ /opt/airflow/dags/
