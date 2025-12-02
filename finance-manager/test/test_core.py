import pytest
from app.core import load_seed, add_transaction, update_budget, account_balance

@pytest.fixture
def sample_data():
    return {
        "accounts": [{"id": "a1", "name": "Card"}, {"id": "a2", "name": "Cash"}],
        "categories": [{"id": "c1", "name": "Food"}],
        "transactions": [
            {"id": "t1", "acc_id": "a1", "amount": -100},
            {"id": "t2", "acc_id": "a1", "amount": 200},
        ],
        "budgets": [{"id": "b1", "limit": 500}],
    }

def test_add_transaction(sample_data):
    trans = tuple(sample_data["transactions"])
    new_t = {"id": "t3", "acc_id": "a2", "amount": 300}
    result = add_transaction(trans, new_t)
    assert len(result) == 3
    assert result[-1]["id"] == "t3"

def test_update_budget(sample_data):
    budgets = tuple(sample_data["budgets"])
    updated = update_budget(budgets, "b1", 800)
    assert updated[0]["limit"] == 800
    assert budgets[0]["limit"] == 500  # неизменяемость

def test_account_balance(sample_data):
    trans = tuple(sample_data["transactions"])
    assert account_balance(trans, "a1") == 100  # -100 + 200 = 100

def test_load_seed(tmp_path, sample_data):
    file = tmp_path / "seed.json"
    import json
    with open(file, "w", encoding="utf-8") as f:
        json.dump(sample_data, f)
    acc, cat, trans, bud = load_seed(str(file))
    assert len(acc) == 2
    assert len(trans) == 2
