import logging
import pandas as pd

logger=logging.getLogger(__name__)

COLUMN_MAP = {
    "time": "weather_date",
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "temperature_2m_mean": "temp_mean_c",
    "precipitation_sum": "precipitation_mm",
    "wind_speed_10m_max": "wind_speed_max_kmh",
}

MEASURE_COLS=[c for c in COLUMN_MAP.values() if c !='weather_date']
OUTPUT_COL=["city_id","weather_date",*MEASURE_COLS]

def to_dataframe(api_json,city_id):
    daily = api_json.get("daily")
    if not daily or not daily.get("time"):
        return pd.DataFrame(columns=OUTPUT_COL)

    df=pd.DataFrame(daily).rename(columns=COLUMN_MAP)
    df['weather_date']=pd.to_datetime(df['weather_date']).dt.date
    df['city_id']=city_id
    df=df.dropna(subset=MEASURE_COLS,how='all') # Drop If all the values in rows are null
    bad = (df['temp_max_c'] < df['temp_min_c']) | (df['precipitation_mm'] < 0)
    if bad.any():
        logger.warning("Dropping %d invalid row for the city %s",bad.sum(),city_id)
        df=df[~bad]
    df=df.drop_duplicates(subset=['city_id','weather_date'])
    return df[OUTPUT_COL]


