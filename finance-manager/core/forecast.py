from functools import lru_cache
from statistics import mean
import time

def _make_hashable(transactions):
    return tuple(tuple(sorted(t.items())) for t in transactions)

@lru_cache
def forecast_expenses(cat_id: str, transactions_hashable: tuple, period: int) -> int:
    transactions = [dict(t) for t in transactions_hashable]
    amounts = [abs(t["amount"]) for t in transactions if t["cat_id"] == cat_id and t["amount"] < 0]
    if not amounts:
        return 0
    n = min(len(amounts), period)
    return int(mean(amounts[-n:]))

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, round((end - start) * 1000, 2)
