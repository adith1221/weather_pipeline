import logging
from datetime import date, timedelta

from src.extract import fetch_daily_weather
from src.transform import to_dataframe
from src.load import get_cities, get_connection, get_last_loaded_date, upsert_weather

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("pipeline")

HISTORY_DAYS = 730
ARCHIVE_LAG_DAYS = 5
REPROCESS_DAYS = 2


def run():
    end_date = date.today() - timedelta(days=ARCHIVE_LAG_DAYS)
    conn = get_connection()
    try:
        for city_id, city_name, lat, lon in get_cities(conn):
            last = get_last_loaded_date(conn, city_id)
            if last is None:
                start_date = end_date - timedelta(days=HISTORY_DAYS)
            else:
                start_date = last - timedelta(days=REPROCESS_DAYS)

            if start_date > end_date:
                logger.info("%s is up to date", city_name)
                continue

            logger.info("%s: fetching %s to %s", city_name, start_date, end_date)
            raw = fetch_daily_weather(float(lat), float(lon), start_date.isoformat(), end_date.isoformat())
            df = to_dataframe(raw, city_id)
            count = upsert_weather(conn, df)
            logger.info("%s: upserted %d rows", city_name, count)
    finally:
        conn.close()


if __name__ == "__main__":
    run()