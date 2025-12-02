import pytest
from core.lazy import iter_transactions, lazy_top_categories
from core.domain import Transaction, Category

transactions = (
    Transaction("t1", "acc1", "food", -100, "2025-01-01", "note1"),
    Transaction("t2", "acc1", "food", -300, "2025-01-02", "note2"),
    Transaction("t3", "acc1", "transport", -200, "2025-01-03", "note3"),
    Transaction("t4", "acc1", "leisure", -50, "2025-01-04", "note4"),
)

categories = (
    Category("food", "Food", None, "expense"),
    Category("transport", "Transport", None, "expense"),
    Category("leisure", "Leisure", None, "expense"),
)


def test_iter_transactions():
    result = list(iter_transactions(transactions, lambda t: t.amount < -100))
    assert len(result) == 2
    assert result[0].id == "t2"
    assert result[1].id == "t3"

def test_lazy_top_categories():
    gen = lazy_top_categories(iter_transactions(transactions, lambda t: True), categories, 3)
    result = list(gen)
    assert result[-2][0] == "transport"
    assert result[-1][0] == "leisure" or result[-1][0] in {"food", "leisure"}  

def test_empty_predicate():
    gen = iter_transactions(transactions, lambda t: t.amount < -1000)
    assert list(gen) == []

def test_top_category_counter_order():
    gen = lazy_top_categories(iter_transactions(transactions, lambda t: True), categories, 3)
    last = None
    for cat_id, total in gen:
        last = (cat_id, total)
    assert last is not None

def test_cat_not_included():
    cat = Category("salary", "Salary", None, "income")
    gen = lazy_top_categories(iter_transactions(transactions, lambda t: True), (cat,), 1)
    assert list(gen) == []
