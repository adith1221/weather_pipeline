# Here What we are doing is trying to get the possible way the error can happen so in future if any changes made we can find the error
import math
from src.transform import to_dataframe

#Sample Json Data For Testing
def sample_json(**overrides):
    daily = {
        "time": ["2026-10-01", "2026-10-02"],
        "temperature_2m_max": [30.0, 29.0],
        "temperature_2m_min": [20.0, 19.5],
        "temperature_2m_mean": [25.0, 24.0],
        "precipitation_sum": [0.0, 5.2],
        "wind_speed_10m_max": [12.0, 15.0],
    }
    daily.update(overrides)
    return {'daily':daily}


def test_one_row_per_day():
    df = to_dataframe(sample_json(), city_id=1)
    assert len(df) == 2
    assert list(df["city_id"]) == [1, 1]

def test_invalid_rows_are_dropped():
    df = to_dataframe(sample_json(temperature_2m_max=[10.0, 29.0]), city_id=1)
    assert len(df) == 1
    # assert df['temperature_2m_max'] > df['temperature_2m_min'].all()

def test_nulls_are_kept_as_missing():
    df = to_dataframe(sample_json(precipitation_sum=[None, 5.2]), city_id=1)
    assert len(df) == 2
    assert math.isnan(df.iloc[0]["precipitation_mm"])

def test_empty_response():
    df = to_dataframe({}, city_id=1)
    assert df.empty    