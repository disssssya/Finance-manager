from collections import defaultdict
from typing import Iterable, Tuple, Iterator
from core.domain import Transaction, Category

# ================== Трансформы для фильтрации и суммирования ==================

def filter_month(data, month="2025-01"):
    """
    Фильтрует транзакции по указанному месяцу.
    data: список словарей, каждый словарь — транзакция с ключом 'month'
    month: строка формата "YYYY-MM"
    """
    return [t for t in data if t.get("month") == month]

def sum_amounts(data):
    """
    Суммирует поле 'amount' для всех элементов списка data.
    """
    return sum(t.get("amount", 0) for t in data)

def sum_by_category(data, cat_id):
    """
    Суммирует поле 'amount' для всех элементов списка data с конкретным cat_id.
    """
    return sum(t.get("amount", 0) for t in data if t.get("cat_id") == cat_id)

# ================== Ленивая обработка транзакций ==================

def iter_transactions(trans: Tuple[Transaction, ...], pred) -> Iterable[Transaction]:
    """
    Ленивая фильтрация транзакций по предикату.
    trans: кортеж объектов Transaction
    pred: функция-предикат, возвращает True/False
    """
    for t in trans:
        if pred(t):
            yield t

def lazy_top_categories(
    trans: Iterable[Transaction],
    cats: Tuple[Category, ...],
    k: int
) -> Iterator[tuple[str, int]]:
    """
    Потоковый подсчёт расходов по категориям, с yield-выводом топ-k категорий.
    trans: итератор объектов Transaction
    cats: кортеж объектов Category
    k: количество топ категорий
    """
    cat_map = {c.id: c.name for c in cats}
    totals = defaultdict(int)

    for t in trans:
        totals[t.cat_id] += abs(t.amount)

    sorted_cats = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    for cat_id, total in sorted_cats[:k]:
        yield (cat_map.get(cat_id, f"cat_{cat_id}"), total)
