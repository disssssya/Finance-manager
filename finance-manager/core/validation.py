from core.maybe_either import Left, Right, Maybe

# ====== Классы данных ======
class Account:
    def __init__(self, acc_id, name):
        self.acc_id = acc_id
        self.name = name

class Category:
    def __init__(self, cat_id, name):
        self.cat_id = cat_id
        self.name = name

class Transaction:
    def __init__(self, acc_id, cat_id, amount):
        self.acc_id = acc_id
        self.cat_id = cat_id
        self.amount = amount

class Budget:
    def __init__(self, cat_id, limit):
        self.cat_id = cat_id
        self.limit = limit


def safe_category(cats, cat_id) -> Maybe:
    found = next((c for c in cats if c.cat_id == cat_id), None)
    return Maybe(found)


def validate_transaction(t: Transaction, accs: tuple[Account, ...], cats: tuple[Category, ...]):
    acc_ok = any(a.acc_id == t.acc_id for a in accs)
    if not acc_ok:
        return Left({"error": f"Account {t.acc_id} not found"})

    cat_ok = any(c.cat_id == t.cat_id for c in cats)
    if not cat_ok:
        return Left({"error": f"Category {t.cat_id} not found"})

    return Right(t)


def check_budget(b: Budget, trans: tuple[Transaction, ...]):
    total = sum(t.amount for t in trans if t.cat_id == b.cat_id)
    if total > b.limit:
        return Left({"error": f"Budget exceeded for category {b.cat_id}. Limit={b.limit}, Total={total}"})
    return Right(b)


def validate_pipeline(t: Transaction, accs, cats, budgets, all_trans):
    result = (
        validate_transaction(t, accs, cats)
        .bind(lambda valid_t: check_budget(
            next((b for b in budgets if b.cat_id == valid_t.cat_id), Budget(valid_t.cat_id, 999999)),
            all_trans + [valid_t]
        ))
    )
    return result
