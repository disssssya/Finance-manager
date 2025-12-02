from typing import Tuple, Iterable, Iterator
from collections import Counter
from .domain import Transaction, Category

def iter_transactions(trans: Tuple[Transaction, ...], pred) -> Iterable[Transaction]:
    for t in trans:
        if pred(t):
            yield t

def lazy_top_categories(trans: Iterable[Transaction], cats: Tuple[Category, ...], k: int) -> Iterator[tuple[str, int]]:
    counter = Counter()
    cat_ids = {c.id for c in cats}
    for t in trans:
        if t.cat_id in cat_ids:
            counter[t.cat_id] += t.amount
            yield t.cat_id, counter[t.cat_id]
