from datetime import datetime

def by_category(cat_id: str):
    def f(t):
        return t["cat_id"] == cat_id
    return f

def by_date_range(start: str, end: str):
    s = datetime.fromisoformat(start)
    e = datetime.fromisoformat(end)
    def f(t):
        d = datetime.fromisoformat(t["date"])
        return s <= d <= e
    return f

def by_amount_range(min_amt: int, max_amt: int):
    def f(t):
        return min_amt <= abs(t["amount"]) <= max_amt
    return f
from core.maybe_either import Just, Nothing

def safe_category(cats, cat_id):
    found = next((c for c in cats if c.id == cat_id), None)
    return Just(found) if found else Nothing()
