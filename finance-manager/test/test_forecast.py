from core.forecast import forecast_expenses, measure_time, _make_hashable

transactions = [
    {"cat_id": "food", "amount": -100},
    {"cat_id": "food", "amount": -200},
    {"cat_id": "food", "amount": -300},
]
hashable = _make_hashable(transactions)

def test_forecast_basic():
    result = forecast_expenses("food", hashable, 3)
    assert result == 200

def test_forecast_empty():
    result = forecast_expenses("rent", hashable, 3)
    assert result == 0

def test_cache_speed():
    uncached, t1 = measure_time(forecast_expenses.__wrapped__, "food", hashable, 3)
    cached, t2 = measure_time(forecast_expenses, "food", hashable, 3)
    assert t2 <= t1
