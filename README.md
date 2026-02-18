# Weather Tracker

Сервис забирает данные по [OpenWeatherMap API](https://openweathermap.org/api), раз в N минут опрашивает и сохраняет в данные базу. 
Ошибки и таймауты пишутся в отдельный лог-файл.

## Быстрый старт

**1.** Получить API-ключ на сайте [openweathermap.org](https://openweathermap.org/api).

**2.** Переименовать `.env.example` на `.env`, вставить свой `WEATHER_API_KEY`.

**3.** Собрать докер, таблицы создаются автоматически при первом запуске:

```bash
docker-compose up -d --build
```

**4.** Зайти в **psql** и отправить запрос:

```
docker-compose exec db psql -U postgres -d weather_db
```

SQL-запрос:

```bash
SELECT
    r.id AS request_id,
    r.city,
    r.requested_at,
    r.status,
    resp.temperature,
    resp.feels_like,
    resp.humidity,
    resp.description,
    resp.wind_speed,
    resp.received_at
FROM requests r
LEFT JOIN responses resp ON resp.request_id = r.id
ORDER BY r.requested_at DESC;
```
