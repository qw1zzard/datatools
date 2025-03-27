import csv
import logging
import os
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv('OPENWEATHER_API_KEY', '')
CITIES: list[str] = ['Moscow', 'Saint Petersburg', 'Novosibirsk']

API_URL: str = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
CSV_PATH: str = '/opt/airflow/spark/weather_data.csv'


def fetch_weather_data():
    results = []

    for city in CITIES:
        response = requests.get(API_URL.format(city=city, api_key=API_KEY))

        if response.status_code == 200:
            temp = response.json()['main']['temp']
            results.append((city, temp))
            logging.info(f'{city}: {temp}°C')
        else:
            logging.error(
                f'Failed to fetch weather data for {city}: {response.status_code}'
            )

    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['city', 'temperature'])
        writer.writerows(results)

    logging.info(f'Data saved to {CSV_PATH}')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 26),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'fetch_weather_data',
    default_args=default_args,
    description='Сбор и анализ данных о температуре с помощью Spark',
    schedule_interval=timedelta(hours=1),
    catchup=False,
)

fetch_weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag,
)

spark_task = SparkSubmitOperator(
    task_id='analyze_weather',
    application='/opt/airflow/spark/analyze_weather.py',
    conn_id='spark_default',
    verbose=True,
    dag=dag,
)

fetch_weather_task >> spark_task
