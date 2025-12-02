from core.validation import (
    Account, Category, Transaction, Budget,
    safe_category, validate_transaction, check_budget, validate_pipeline
)
from core.maybe_either import Left, Right, Maybe


def test_safe_category_found():
    cats = [Category(1, "Food"), Category(2, "Transport")]
    m = safe_category(cats, 1)
    assert isinstance(m, Maybe)
    assert m.get_or_else(None).name == "Food"


def test_safe_category_not_found():
    cats = [Category(1, "Food")]
    m = safe_category(cats, 5)
    assert m.get_or_else("none") == "none"


def test_validate_transaction_ok():
    accs = [Account(1, "Cash")]
    cats = [Category(10, "Food")]
    t = Transaction(1, 10, 100)
    result = validate_transaction(t, accs, cats)
    assert isinstance(result, Right)


def test_validate_transaction_fail():
    accs = [Account(1, "Cash")]
    cats = [Category(10, "Food")]
    t = Transaction(2, 10, 100)
    result = validate_transaction(t, accs, cats)
    assert isinstance(result, Left)


def test_check_budget():
    b = Budget(10, 200)
    trans = [Transaction(1, 10, 50), Transaction(1, 10, 180)]
    result = check_budget(b, trans)
    assert isinstance(result, Left)


def test_pipeline_full_ok():
    accs = [Account(1, "Cash")]
    cats = [Category(10, "Food")]
    budgets = [Budget(10, 300)]
    trans = [Transaction(1, 10, 100)]
    t = Transaction(1, 10, 50)
    result = validate_pipeline(t, accs, cats, budgets, trans)
    assert isinstance(result, Right)


def test_pipeline_budget_exceeded():
    accs = [Account(1, "Cash")]
    cats = [Category(10, "Food")]
    budgets = [Budget(10, 150)]
    trans = [Transaction(1, 10, 100)]
    t = Transaction(1, 10, 100)
    result = validate_pipeline(t, accs, cats, budgets, trans)
    assert isinstance(result, Left)
