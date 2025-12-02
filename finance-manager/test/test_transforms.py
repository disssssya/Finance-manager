from core.domain import Transaction, Category
from core.lazy import lazy_top_categories, iter_transactions

def test_lazy_top_categories_simple():
    trans = (
        Transaction("t1", "a1", "food", -100, "2025-01-01", "note"),
        Transaction("t2", "a1", "transport", -300, "2025-01-02", "note"),
        Transaction("t3", "a1", "food", -200, "2025-01-03", "note"),
    )
    cats = (
        Category("food", "Food", None, "expense"),
        Category("transport", "Transport", None, "expense"),
    )
    gen = lazy_top_categories(iter_transactions(trans, lambda t: True), cats, 2)
    result = list(gen)
    assert result[-1][0] == "food"

def test_lazy_top_categories_limit_k():
    trans = (
        Transaction("t1", "a1", "a", -100, "2025-01-01", "note"),
        Transaction("t2", "a1", "b", -300, "2025-01-02", "note"),
        Transaction("t3", "a1", "c", -400, "2025-01-03", "note"),
    )
    cats = (
        Category("a", "A", None, "expense"),
        Category("b", "B", None, "expense"),
        Category("c", "C", None, "expense"),
    )
    gen = lazy_top_categories(iter_transactions(trans, lambda t: True), cats, 2)
    result = list(gen)
    assert result[-1][0] in {"b", "c"}

def test_lazy_combined_pipeline():
    trans = (
        Transaction("t1", "a1", "groceries", -50, "2025-01-01", "note"),
        Transaction("t2", "a1", "tech", -500, "2025-01-02", "note"),
        Transaction("t3", "a2", "fun", -100, "2025-01-03", "note"),
    )
    cats = (
        Category("groceries", "Groceries", None, "expense"),
        Category("tech", "Tech", None, "expense"),
        Category("fun", "Fun", None, "expense"),
    )
    gen = lazy_top_categories(iter_transactions(trans, lambda t: True), cats, 3)
    result = list(gen)
    assert len(result) > 0
