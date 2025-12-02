from core.filters import by_category, by_amount_range, by_date_range

transactions = [
    {"cat_id": "food", "amount": -100, "date": "2024-10-01"},
    {"cat_id": "rent", "amount": -500, "date": "2024-10-05"},
]

def test_by_category():
    f = by_category("food")
    assert list(filter(f, transactions))[0]["cat_id"] == "food"

def test_by_amount_range():
    f = by_amount_range(50, 150)
    assert len(list(filter(f, transactions))) == 1

def test_by_date_range():
    f = by_date_range("2024-10-01", "2024-10-03")
    assert len(list(filter(f, transactions))) == 1
