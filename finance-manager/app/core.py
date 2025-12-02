from functools import reduce
import json

def load_seed(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (
        tuple(data["accounts"]),
        tuple(data["categories"]),
        tuple(data["transactions"]),
        tuple(data["budgets"]),
    )

def add_transaction(trans: tuple, t: dict):
    return trans + (t,)

def update_budget(budgets: tuple, bid: str, new_limit: int):
    return tuple(
        b | {"limit": new_limit} if b["id"] == bid else b
        for b in budgets
    )

def account_balance(trans: tuple, acc_id: str):
    return reduce(lambda acc, t: acc + t["amount"] if t["acc_id"] == acc_id else acc, trans, 0)
