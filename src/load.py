import psycopg2
from psycopg2.extras import execute_values

from src.config import DB_CONFIG

UPSERT_QUERY='''
    INSERT INTO daily_weather (
    city_id,weather_date,temp_max_c,temp_min_c,temp_mean_c,precipitation_mm,wind_speed_max_kmh
    ) values %s
    ON CONFLICT (city_id,weather_date) DO UPDATE SET
    temp_max_c=EXCLUDED.temp_max_c,
    temp_min_c=EXCLUDED.temp_min_c,
    temp_mean_c=EXCLUDED.temp_mean_c,
    precipitation_mm=EXCLUDED.precipitation_mm,
    wind_speed_max_kmh=EXCLUDED.wind_speed_max_kmh,
    loaded_at=NOW();
'''

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_cities(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT city_id, city_name, latitude, longitude FROM cities ORDER BY city_id")
        return cur.fetchall()
    
def get_last_loaded_date(conn,city_id):
    with conn.cursor() as cur:
        cur.execute("select max(weather_date) from daily_weather where city_id=%s",(city_id,))
        return cur.fetchone()[0]
    
def upsert_weather(conn,df):
    if df.empty:
        return 0
    rows = df.astype(object).where(df.notna(),None).values.tolist()
    with conn.cursor() as cur:
        execute_values(cur,UPSERT_QUERY,rows)
    conn.commit()
    return len(rows)
