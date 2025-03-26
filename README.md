# datatools - Airflow DAG для сбора данных о погоде

## Как запустить проект

Убедитесь, что у вас установлен и запущен Docker Engine, затем выполните команду:

```sh
docker compose up --build -d
```

Чтобы остановить контейнеры, используйте:

```sh
docker compose down
```

## Доступ к Airflow

- Веб-интерфейс: [http://localhost:8080](http://localhost:8080)
- Логин: `airflow`
- Пароль: `airflow`

## ЛР 1. Airflow + docker compose

DAG `fetch_weather_data` собирает данные о средней температуре в нескольких крупных
городах с использованием OpenWeather API. Запуск происходит автоматически каждые 3 часа.

## Настройка API-ключа

Перед запуском добавьте API-ключ в файл `.env` в корне проекта:

```sh
OPENWEATHER_API_KEY=<YOUR_OPENWEATHER_API_KEY>
```
