from functools import reduce
from typing import Callable

def compose(*funcs: Callable):
    """Составление функций справа налево: compose(f, g)(x) = f(g(x))"""
    def composed(x):
        return reduce(lambda acc, f: f(acc), reversed(funcs), x)
    return composed

def pipe(x, *funcs: Callable):
    """Пропуск значения через функции слева направо: pipe(x, f, g) = g(f(x))"""
    return reduce(lambda acc, f: f(acc), funcs, x)
