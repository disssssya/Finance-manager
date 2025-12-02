from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Account:
    id: str
    name: str
    balance: int  # начальный баланс, целое (например в тенге)
    currency: str  # "KZT"

@dataclass(frozen=True)
class Category:
    id: str
    name: str
    parent_id: Optional[str]  # None если корневая
    type: str  # "income" или "expense"

@dataclass(frozen=True)
class Transaction:
    id: str
    account_id: str
    cat_id: str
    amount: int    # положительное = доход, отрицательное = расход
    ts: str        # ISO-like: "YYYY-MM-DD"
    note: Optional[str] = None

@dataclass(frozen=True)
class Budget:
    id: str
    cat_id: str
    limit: int     # лимит (целое)
    period: str    # "month" или "week"

@dataclass(frozen=True)
class Event:
    id: str
    ts: str
    name: str
    payload: dict
