import logging
import os
from datetime import datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
CITIES = ['Moscow', 'Saint Petersburg', 'Novosibirsk']
API_URL = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'


def fetch_weather_data():
    results = {}
    for city in CITIES:
        response = requests.get(API_URL.format(city=city, api_key=API_KEY))
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            results[city] = temp
            logging.info(f'{city}: {temp}°C')
        else:
            logging.error(
                f'Failed to fetch weather data for {city}: {response.status_code}'
            )
    return results


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
    description='Сбор данных о температуре в крупных городах',
    schedule_interval=timedelta(hours=3),
    catchup=False,
)

fetch_weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag,
)

fetch_weather_task
