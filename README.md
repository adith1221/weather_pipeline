# Weather Data Pipeline (Open-Meteo → PostgreSQL)

An ETL pipeline that collects 2 years of daily weather for 6 Indian cities from the free
Open-Meteo API, cleans it with pandas, and loads it into PostgreSQL running in Docker.
It loads incrementally and is safe to rerun (idempotent). Analysis is done in SQL.

## Architecture

```
Open-Meteo API → extract.py → transform.py → load.py → PostgreSQL (Docker) → SQL analysis
```

## Tech stack

Python (requests, pandas, psycopg2), PostgreSQL 16, Docker Compose, pytest, SQL (CTEs, window functions)

## How to run

Requirements: Python 3.10+, Docker Desktop

```bash
git clone https://github.com/YOUR-USERNAME/weather-pipeline.git
cd weather-pipeline
cp .env.example .env 
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up -d
python -m src.pipeline
python -m pytest  
```

## Design decisions

- **Composite primary key `(city_id, weather_date)`** guarantees one row per city per day.
- **Upsert (`INSERT ... ON CONFLICT DO UPDATE`)** makes reruns safe, with no duplicates.
- **Incremental loading:** the first run loads 730 days; later runs start 2 days before
  the last loaded date, to pick up any corrected values.
- **Retries with exponential backoff** handle temporary network failures.
- **Data validation:** rows where max temperature < min temperature, or with negative
  rain, are dropped and logged.
- **Separate extract / transform / load modules** keep each step simple and testable.


## What I'd improve next

- Schedule daily runs with Airflow
- Add dbt models for monthly summary tables
- Build a dashboard in Metabase or Streamlit
- Run tests automatically on every push with GitHub Actions
