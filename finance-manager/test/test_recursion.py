from core.recursion import flatten_categories, sum_expenses_recursive

cats = [
    {"id": "root", "parent_id": None},
    {"id": "food", "parent_id": "root"},
    {"id": "snacks", "parent_id": "food"},
]

transactions = [
    {"cat_id": "food", "amount": -200},
    {"cat_id": "snacks", "amount": -50},
]

def test_flatten_categories():
    flat = flatten_categories(cats, "root")
    ids = [c["id"] for c in flat]
    assert ids == ["food", "snacks"]

def test_sum_expenses_recursive():
    total = sum_expenses_recursive(cats, transactions, "root")
    assert total == 250
