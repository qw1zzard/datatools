FROM apache/airflow:2.10.5

WORKDIR /opt/airflow

USER root
RUN apt update && apt -y install procps default-jre

USER airflow
COPY dags/ /opt/airflow/dags/
COPY spark/ /opt/airflow/spark/

RUN pip install apache-airflow-providers-apache-spark
