def flatten_categories(cats, root=None):
    result = []
    for c in cats:
        if c.get("parent_id") == root:
            result.append(c)
            result.extend(flatten_categories(cats, c["id"]))
    return result

def sum_expenses_recursive(cats, trans, root_id):
    subs = [c for c in cats if c.get("parent_id") == root_id]
    total = sum(-t["amount"] for t in trans if t["cat_id"] == root_id and t["amount"] < 0)
    for s in subs:
        total += sum_expenses_recursive(cats, trans, s["id"])
    return total
