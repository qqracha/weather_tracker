import json
import logging
import os
import time
from datetime import datetime
import requests
from sqlalchemy.exc import OperationalError

from config import INTERVAL_MINUTES, LOG_FILE, WEATHER_API_KEY, WEATHER_API_URL, WEATHER_CITY
from database import Request, Response, get_session, init_db

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

def fetch_weather() -> dict:
    params = {"q": WEATHER_CITY, "appid": WEATHER_API_KEY, "units": "metric", "lang": "ru"}
    response = requests.get(WEATHER_API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def run_once() -> None:
    try:
        session = get_session()
    except OperationalError as e:
        logger.error("Database connection error: %s", e)
        return
    with session:
        request = Request(city=WEATHER_CITY, requested_at=datetime.now(), status="success")
        session.add(request)
        session.flush()
        try:
            data = fetch_weather()
            main = data.get("main", {})
            wind = data.get("wind", {})
            description = data.get("weather", [{}])[0].get("description", "")
            session.add(
                Response(
                    request_id=request.id,
                    temperature=main.get("temp"),
                    feels_like=main.get("feels_like"),
                    humidity=main.get("humidity"),
                    description=description,
                    wind_speed=wind.get("speed"),
                    raw_json=json.dumps(data),
                    received_at=datetime.utcnow(),
                )
            )
            session.commit()
            logger.info(
                "Saved weather for %s: %.1f°C, %s",
                WEATHER_CITY,
                main.get("temp", 0),
                description,
            )

        except requests.exceptions.Timeout as e:
            logger.error("Request timeout: %s", e)
            request.status = "timeout"
            session.commit()
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: %s", e)
            request.status = "connection_error"
            session.commit()
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error: %s", e)
            request.status = "http_error"
            session.commit()
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            session.rollback()

def main() -> None:
    logger.info("Starting weather tracker (interval: %d min)", INTERVAL_MINUTES)
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)
        return
    while True:
        run_once()
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
