import os
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv("LOG_FILE", "logs/errors.log")
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", "5"))
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_CITY = os.getenv("WEATHER_CITY", "Moscow")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'weather_db')}"
)
