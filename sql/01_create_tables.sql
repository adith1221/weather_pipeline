   CREATE TABLE IF NOT EXISTS cities (
       city_id     SERIAL PRIMARY KEY,
       city_name   VARCHAR(50) UNIQUE NOT NULL,
       state       VARCHAR(50),
       latitude    NUMERIC(7,4) NOT NULL,
       longitude   NUMERIC(7,4) NOT NULL
   );

   INSERT INTO cities (city_name, state, latitude, longitude) VALUES
       ('Bengaluru', 'Karnataka',   12.9716, 77.5946),
       ('Mumbai',    'Maharashtra', 19.0760, 72.8777),
       ('Delhi',     'Delhi',       28.6139, 77.2090),
       ('Chennai',   'Tamil Nadu',  13.0827, 80.2707),
       ('Kolkata',   'West Bengal', 22.5726, 88.3639),
       ('Hyderabad', 'Telangana',   17.3850, 78.4867)
   ON CONFLICT (city_name) DO NOTHING;

   CREATE TABLE IF NOT EXISTS daily_weather (
       city_id            INT  NOT NULL REFERENCES cities(city_id),
       weather_date       DATE NOT NULL,
       temp_max_c         NUMERIC(4,1),
       temp_min_c         NUMERIC(4,1),
       temp_mean_c        NUMERIC(4,1),
       precipitation_mm   NUMERIC(6,1),
       wind_speed_max_kmh NUMERIC(5,1),
       loaded_at          TIMESTAMP DEFAULT NOW(),
       PRIMARY KEY (city_id, weather_date)
   );