import logging
import time

import requests

from src.config import API_URL, DAILY_VARS, TIMEZONE

logger = logging.getLogger(__name__)


def fetch_daily_weather(lat, lon, start_date, end_date, max_retries=3):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_VARS),
        "timezone": TIMEZONE,
    }
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(API_URL, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            if attempt == max_retries:
                logger.error("All %d attempts failed: %s", max_retries, e)
                raise
            wait = 2 ** attempt
            logger.warning("Attempt %d failed (%s). Retrying in %ds", attempt, e, wait)
            time.sleep(wait)


