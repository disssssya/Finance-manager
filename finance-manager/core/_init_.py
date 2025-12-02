# core/__init__.py
from .lazy import (
    lazy_top_categories,
    lazy_large_transactions, 
    lazy_transactions_by_date,
    lazy_income_transactions,
    lazy_expense_transactions,
    lazy_transactions_by_category, 
    lazy_complex_pipeline,
    demonstrate_lazy_vs_eager
)

__all__ = [
    'lazy_top_categories',
    'lazy_large_transactions',
    'lazy_transactions_by_date', 
    'lazy_income_transactions',
    'lazy_expense_transactions',
    'lazy_transactions_by_category',
    'lazy_complex_pipeline',
    'demonstrate_lazy_vs_eager'
]