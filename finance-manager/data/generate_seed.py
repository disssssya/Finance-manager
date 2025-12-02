import json
import random
from core.domain import Account, Category, Transaction, Budget

random.seed(42)

def generate_accounts():
    return (
        Account("acc1", "Карта"),
        Account("acc2", "Наличные"),
        Account("acc3", "Депозит"),
    )

def generate_categories():
    return (
        Category("food", "Питание", None),
        Category("rest", "Рестораны", "food"),
        Category("groceries", "Продукты", "food"),
        Category("transport", "Транспорт", None),
        Category("taxi", "Такси", "transport"),
        Category("bus", "Автобус", "transport"),
        Category("fun", "Развлечения", None),
        Category("movies", "Кино", "fun"),
        Category("games", "Игры", "fun"),
        Category("edu", "Образование", None),
    )

def generate_transactions(accounts, categories, n=120):
    trans = []
    for i in range(n):
        acc = random.choice(accounts)
        cat = random.choice(categories)
        amount = random.randint(-5000, 20000)  # расходы или доходы
        ts = f"2025-01-{random.randint(1,28):02d}"
        trans.append(Transaction(f"t{i}", acc.id, cat.id, amount, ts))
    return tuple(trans)

def generate_budgets():
    return (
        Budget("b1", "food", 50000, "month"),
        Budget("b2", "transport", 20000, "month"),
        Budget("b3", "fun", 30000, "month"),
    )

def save_seed(path="data/seed.json"):
    accounts = generate_accounts()
    categories = generate_categories()
    transactions = generate_transactions(accounts, categories)
    budgets = generate_budgets()

    data = {
        "accounts": [a._asdict() for a in accounts],
        "categories": [c._asdict() for c in categories],
        "transactions": [t._asdict() for t in transactions],
        "budgets": [b._asdict() for b in budgets],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    save_seed()
