import pytest
from core.frp import EventBus
from core.frp import update_balance, check_budget, create_alert

def test_eventbus_subscribe_publish():
    bus = EventBus()
    bus.subscribe("TRANSACTION_ADDED", update_balance)
    results = bus.publish("TRANSACTION_ADDED", {"account_id": "a1", "amount": 100})
    assert results[0] == {"a1": 100}

def test_multiple_subscribers():
    bus = EventBus()
    bus.subscribe("TRANSACTION_ADDED", update_balance)
    bus.subscribe("TRANSACTION_ADDED", create_alert)
    results = bus.publish("TRANSACTION_ADDED", {"account_id": "a1", "amount": 50})
    assert len(results) == 2
    assert results[0] == {"a1": 50}
    assert "TRANSACTION_ADDED" in results[1]["alerts"][0]

def test_check_budget():
    bus = EventBus()
    bus.subscribe("TRANSACTION_ADDED", check_budget)
    results = bus.publish("TRANSACTION_ADDED", {"cat_id": "food", "amount": 200})
    assert results[0] == {"food": 200}

def test_no_subscribers():
    bus = EventBus()
    results = bus.publish("UNKNOWN_EVENT", {"x": 1})
    assert results == []

def test_multiple_events_sequence():
    bus = EventBus()
    bus.subscribe("TRANSACTION_ADDED", update_balance)
    bus.subscribe("BUDGET_ALERT", create_alert)
    res1 = bus.publish("TRANSACTION_ADDED", {"account_id": "a1", "amount": 100})
    res2 = bus.publish("BUDGET_ALERT", {"cat_id": "food", "amount": 500})
    assert res1[0]["a1"] == 100
    assert "BUDGET_ALERT" in res2[0]["alerts"][0]
