import streamlit as st
import json
import os
from dataclasses import dataclass, asdict
from functools import reduce
import plotly.express as px
from typing import Optional, Tuple, List

DATA_FILE = "data/seed.json"

def fmt(x):
    try:
        x = float(x)
        if x.is_integer():
            return f"{int(x):,}".replace(",", " ")
        else:
            return f"{x:,.2f}".replace(",", " ")
    except:
        return str(x)



# -------------------- Immutable models (dataclasses) --------------------
@dataclass(frozen=True)
class User:
    id: int
    name: str


@dataclass(frozen=True)
class Account:
    id: int
    user_id: Optional[int]
    name: str
    balance: float
    currency: str = "KZT"


@dataclass(frozen=True)
class Category:
    id: int
    user_id: Optional[int]
    name: str
    parent_id: Optional[int] = None


@dataclass(frozen=True)
class Transaction:
    id: int
    user_id: Optional[int]
    acc_id: int
    cat_id: int
    amount: float


@dataclass(frozen=True)
class Budget:
    id: int
    user_id: Optional[int]
    cat_id: int
    limit: float


# -------------------- Pure core functions (operate on tuples) --------------------
def load_seed(path: str) -> Tuple[Tuple[User, ...], Tuple[Account, ...], Tuple[Category, ...], Tuple[Transaction, ...], Tuple[Budget, ...]]:
    """Pure: load json and return tuples of dataclass instances."""
    if not os.path.exists(path):
        return (), (), (), (), ()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    def _u(x): return User(**x)
    def _a(x): return Account(id=x["id"], user_id=x.get("user_id"), name=x.get("name", ""), balance=float(x.get("balance", 0.0)), currency=x.get("currency", "KZT"))
    def _c(x): return Category(id=x["id"], user_id=x.get("user_id"), name=x.get("name", ""), parent_id=x.get("parent_id"))
    def _t(x): return Transaction(id=x["id"], user_id=x.get("user_id"), acc_id=x["acc_id"], cat_id=x["cat_id"], amount=float(x["amount"]))
    def _b(x): return Budget(id=x["id"], user_id=x.get("user_id"), cat_id=x["cat_id"], limit=float(x["limit"]))
    users = tuple(map(_u, data.get("users", [])))
    accounts = tuple(map(_a, data.get("accounts", [])))
    categories = tuple(map(_c, data.get("categories", [])))
    transactions = tuple(map(_t, data.get("transactions", [])))
    budgets = tuple(map(_b, data.get("budgets", [])))
    return users, accounts, categories, transactions, budgets


def add_transaction(trans: Tuple[Transaction, ...], t: Transaction) -> Tuple[Transaction, ...]:
    """Pure: return new tuple with appended transaction"""
    return trans + (t,)


def update_budget(budgets: Tuple[Budget, ...], bid: int, new_limit: float) -> Tuple[Budget, ...]:
    """Pure: return new budgets tuple with updated limit for matching id"""
    return tuple(b if b.id != bid else Budget(id=b.id, user_id=b.user_id, cat_id=b.cat_id, limit=new_limit) for b in budgets)


def account_balance(trans: Tuple[Transaction, ...], acc_id: int) -> float:
    """Use filter + reduce to compute balance for account acc_id"""
    acc_trans = filter(lambda t: t.acc_id == acc_id, trans)  # filter
    return reduce(lambda acc, t: acc + t.amount, acc_trans, 0.0)  # reduce


def total_balance(trans: Tuple[Transaction, ...], accounts: Tuple[Account, ...]) -> float:
    """Use map + reduce to compute total balance across accounts"""
    balances_iter = map(lambda a: account_balance(trans, a.id), accounts)  # map
    return reduce(lambda s, x: s + x, balances_iter, 0.0)


# -------------------- Helpers to convert between dicts (session/json) and dataclasses --------------------
def dicts_to_users(lst: List[dict]) -> Tuple[User, ...]:
    return tuple(User(**u) for u in lst)


def dicts_to_accounts(lst: List[dict]) -> Tuple[Account, ...]:
    return tuple(Account(id=a["id"], user_id=a.get("user_id"), name=a.get("name", ""), balance=float(a.get("balance", 0.0)), currency=a.get("currency", "KZT")) for a in lst)


def dicts_to_categories(lst: List[dict]) -> Tuple[Category, ...]:
    return tuple(Category(id=c["id"], user_id=c.get("user_id"), name=c.get("name", ""), parent_id=c.get("parent_id")) for c in lst)


def dicts_to_transactions(lst: List[dict]) -> Tuple[Transaction, ...]:
    return tuple(Transaction(id=t["id"], user_id=t.get("user_id"), acc_id=t["acc_id"], cat_id=t["cat_id"], amount=float(t["amount"])) for t in lst)


def dicts_to_budgets(lst: List[dict]) -> Tuple[Budget, ...]:
    return tuple(Budget(id=b["id"], user_id=b.get("user_id"), cat_id=b["cat_id"], limit=float(b["limit"])) for b in lst)


def models_to_dicts(seq):
    """General converter: dataclass instances -> list of dicts"""
    return [asdict(x) for x in seq]


def next_id_from_list(lst: List[dict], key="id") -> int:
    if not lst:
        return 1
    return max((item.get(key, 0) for item in lst), default=0) + 1


# -------------------- File IO and session helpers (UI-side) --------------------
def load_data_ui():
    """Load raw json for session_state use (dicts)."""
    if not os.path.exists(DATA_FILE):
        return {"users": [], "accounts": [], "categories": [], "transactions": [], "budgets": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Ошибка загрузки {DATA_FILE}: {e}")
        return {"users": [], "accounts": [], "categories": [], "transactions": [], "budgets": []}


def save_data_ui():
    os.makedirs(os.path.dirname(DATA_FILE) or ".", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "users": st.session_state.get("users", []),
            "accounts": st.session_state.get("accounts", []),
            "categories": st.session_state.get("categories", []),
            "transactions": st.session_state.get("transactions", []),
            "budgets": st.session_state.get("budgets", []),
        }, f, indent=2, ensure_ascii=False)


def refresh_maps():
    st.session_state["accounts_map"] = {a["id"]: a for a in st.session_state.get("accounts", [])}
    st.session_state["categories_map"] = {c["id"]: c for c in st.session_state.get("categories", [])}
    st.session_state["users_map"] = {u["id"]: u for u in st.session_state.get("users", [])}


# -------------------- Initialize session_state --------------------
if "users" not in st.session_state:
    data = load_data_ui()
    st.session_state["users"] = data.get("users", [])
    st.session_state["accounts"] = data.get("accounts", [])
    st.session_state["categories"] = data.get("categories", [])
    st.session_state["transactions"] = data.get("transactions", [])
    st.session_state["budgets"] = data.get("budgets", [])
    refresh_maps()


# -------------------- Sidebar / UI basics --------------------
st.sidebar.title("Finance Manager")

if st.session_state["users"]:
    selected_user = st.sidebar.selectbox(
        "Пользователь",
        [u["id"] for u in st.session_state["users"]],
        format_func=lambda uid: st.session_state["users_map"][uid]["name"]
    )
else:
    selected_user = None

menu = st.sidebar.radio("Menu", ["Overview", "Data", "Reports", "Settings"])


def filter_by_user(data: List[dict], key="user_id"):
    if not selected_user:
        return []
    return [d for d in data if d.get(key) == selected_user]


# -------------------- Overview --------------------
if menu == "Overview":
    st.title("📊 Overview")

    if not selected_user:
        st.info("Нет пользователей. Добавьте пользователя во вкладке Data.")
    else:
        # use filter_by_user on raw session_state dicts
        user_trx = filter_by_user(st.session_state["transactions"])
        if not user_trx:
            st.info("Нет транзакций.")
        else:
            refresh_maps()
            # Build dataclass tuples for pure computations
            trans_tup = dicts_to_transactions(st.session_state["transactions"])
            acc_tup = dicts_to_accounts(filter_by_user(st.session_state["accounts"]))

            income = sum(t.amount for t in trans_tup if t.amount > 0 and t.user_id == selected_user)
            expense = sum(-t.amount for t in trans_tup if t.amount < 0 and t.user_id == selected_user)
            balance = income - expense

            col1, col2, col3 = st.columns(3)
            col1.metric("Доход", f"{fmt(income)} KZT")
            col2.metric("Расход", f"{fmt(expense)} KZT")
            col3.metric("Баланс", f"{fmt(balance)} KZT")

            # --- Расходы по категориям ---
            st.subheader("📌 Расходы по категориям")
            categories_map = {c["id"]: c for c in filter_by_user(st.session_state["categories"])}
            expense_data = []
            for t in trans_tup:
                if t.amount < 0 and t.user_id == selected_user:
                    cat_name = categories_map.get(t.cat_id, {"name": "❓ Unknown"})["name"]
                    expense_data.append({"Категория": cat_name, "Сумма": -t.amount})
            if expense_data:
                fig = px.pie(expense_data, names="Категория", values="Сумма", title="Структура расходов")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Нет расходов для построения диаграммы.")

            # --- Финансовые советы ---
            st.subheader("💡 Финансовые советы")
            advice_list = []
            if income == 0:
                advice_list.append("⚠ Нет регулярного дохода. Сначала стабилизируйте заработок.")
            if expense > income:
                advice_list.append("⚠ Ваши расходы превышают доходы. Попробуйте сократить траты.")
            elif balance < income * 0.05:
                advice_list.append("⚠ У вас почти нет свободных денег. Попробуйте откладывать хотя бы 10% дохода.")
            elif income > expense:
                saving_rate = balance / income if income > 0 else 0
                if saving_rate < 0.1:
                    advice_list.append("💡 Вы живёте по средствам, но откладываете мало. Попробуйте увеличить накопления.")
                elif 0.1 <= saving_rate <= 0.2:
                    advice_list.append("✅ Отличный результат! Вы формируете подушку безопасности.")
                elif saving_rate > 0.2:
                    advice_list.append("🏆 Великолепно! Стоит подумать о долгосрочных инвестициях.")

            categories_total = {}
            for t in trans_tup:
                if t.amount < 0 and t.user_id == selected_user:
                    cat_name = categories_map.get(t.cat_id, {"name": "❓ Unknown"})["name"]
                    categories_total[cat_name] = categories_total.get(cat_name, 0) + (-t.amount)
            if categories_total:
                max_cat = max(categories_total, key=categories_total.get)
                if categories_total[max_cat] > expense * 0.9:
                    advice_list.append(f"⚠ Слишком большая доля трат уходит на категорию '{max_cat}'. Сбалансируйте расходы.")

            if advice_list:
                for adv in advice_list:
                    st.write(adv)
            else:
                st.info("Добавьте больше данных, чтобы получить персональные советы.")


# -------------------- Data --------------------
elif menu == "Data":
    st.title("📂 Data")
    tabs = st.tabs(["Users", "Accounts", "Categories", "Transactions", "Budgets"])

    # --- users ---
    with tabs[0]:
        st.subheader("Пользователи")
        st.table(st.session_state["users"])
        with st.form("add_user"):
            name = st.text_input("Имя пользователя")
            submitted = st.form_submit_button("Добавить")
            if submitted and name:
                new_id = next_id_from_list(st.session_state["users"])
                st.session_state["users"].append({"id": new_id, "name": name})
                save_data_ui()
                refresh_maps()
                st.success("Пользователь добавлен")

    if not selected_user:
        st.warning("Выберите пользователя для работы с данными.")
    else:
        # --- accounts ---
        with tabs[1]:
            st.subheader("Счета")
            accs = filter_by_user(st.session_state["accounts"])
            st.table([{**a, "balance": fmt(a.get("balance", 0.0))} for a in accs])
            with st.form("add_acc"):
                name = st.text_input("Название счёта")
                balance = st.number_input("Баланс", value=0.0)
                submitted = st.form_submit_button("Добавить")
                if submitted and name:
                    new_id = next_id_from_list(st.session_state["accounts"])
                    st.session_state["accounts"].append({
                        "id": new_id, "user_id": selected_user,
                        "name": name, "balance": float(balance), "currency": "KZT"
                    })
                    save_data_ui()
                    refresh_maps()
                    st.success("Счёт добавлен")

        # --- categories ---
        with tabs[2]:
            st.subheader("Категории")
            refresh_maps()
            cats = filter_by_user(st.session_state["categories"])
            categories_table = []
            for c in cats:
                parent_name = "—"
                if c.get("parent_id") is not None:
                    parent = st.session_state["categories_map"].get(c["parent_id"])
                    parent_name = parent["name"] if parent else f"#{c['parent_id']}"
                categories_table.append({
                    "id": c["id"], "user_id": c.get("user_id"),
                    "name": c["name"], "parent": parent_name
                })
            st.table(categories_table)

            with st.form("add_cat"):
                name = st.text_input("Название категории")
                existing = [c["id"] for c in cats]
                options = [None] + existing
                def fmt_parent(pid):
                    if pid is None:
                        return "None"
                    return st.session_state["categories_map"].get(pid, {}).get("name", f"#{pid}")
                parent = st.selectbox("Родительская категория", options, format_func=fmt_parent)
                submitted = st.form_submit_button("Добавить")
                if submitted and name:
                    new_id = next_id_from_list(st.session_state["categories"])
                    st.session_state["categories"].append({
                        "id": new_id, "user_id": selected_user,
                        "name": name, "parent_id": parent
                    })
                    save_data_ui()
                    refresh_maps()
                    st.success("Категория добавлена")

        # --- transactions ---
        with tabs[3]:
            st.subheader("➕ Добавить транзакцию")
            with st.form("add_trx"):
                acc_list = filter_by_user(st.session_state["accounts"])
                cat_list = filter_by_user(st.session_state["categories"])
                if not acc_list or not cat_list:
                    st.warning("Сначала добавьте счёт и категорию.")
                else:
                    acc_id = st.selectbox(
                        "Счёт",
                        [a["id"] for a in acc_list],
                        format_func=lambda aid: st.session_state["accounts_map"][aid]["name"]
                    )
                    cat_id = st.selectbox(
                        "Категория",
                        [c["id"] for c in cat_list],
                        format_func=lambda cid: st.session_state["categories_map"][cid]["name"]
                    )
                    amount = st.number_input("Сумма (+ доход, - расход)", value=0.0)
                    submitted = st.form_submit_button("Добавить")
                    if submitted and amount != 0:
                        # Use pure add_transaction:
                        trans_tup = dicts_to_transactions(st.session_state["transactions"])
                        new_id = next_id_from_list(st.session_state["transactions"])
                        new_t = Transaction(id=new_id, user_id=selected_user, acc_id=acc_id, cat_id=cat_id, amount=float(amount))
                        new_trans_tup = add_transaction(trans_tup, new_t)
                        # write back to session_state as dicts
                        st.session_state["transactions"] = models_to_dicts(new_trans_tup)
                        save_data_ui()
                        refresh_maps()
                        st.success("Транзакция добавлена")
                        st.rerun()

            st.divider()
            trx_list = filter_by_user(st.session_state["transactions"])
            if trx_list:
                st.subheader("📋 Список транзакций")
                trx_display = []
                for t in trx_list:
                    acc_name = st.session_state["accounts_map"].get(t["acc_id"], {}).get("name", f"#{t['acc_id']}")
                    cat_name = st.session_state["categories_map"].get(t["cat_id"], {}).get("name", f"#{t['cat_id']}")
                    trx_display.append({
                        "ID": t["id"], "Счёт": acc_name,
                        "Категория": cat_name, "Сумма": fmt(t["amount"])
                    })
                st.table(trx_display)

                # --- редактор транзакций ---
                st.subheader("✏ Редактировать / удалить транзакцию")
                trx_ids = [t["id"] for t in trx_list]
                selected_trx_id = st.selectbox("Выберите транзакцию", trx_ids)
                transaction = next(t for t in trx_list if t["id"] == selected_trx_id)

                with st.form(f"edit_trx_{selected_trx_id}"):
                    acc_choices = [a["id"] for a in filter_by_user(st.session_state["accounts"])]
                    cat_choices = [c["id"] for c in filter_by_user(st.session_state["categories"])]
                    new_acc = st.selectbox(
                        "Счёт",
                        acc_choices,
                        index=acc_choices.index(transaction["acc_id"]) if transaction["acc_id"] in acc_choices else 0,
                        format_func=lambda aid: st.session_state["accounts_map"][aid]["name"]
                    )
                    new_cat = st.selectbox(
                        "Категория",
                        cat_choices,
                        index=cat_choices.index(transaction["cat_id"]) if transaction["cat_id"] in cat_choices else 0,
                        format_func=lambda cid: st.session_state["categories_map"][cid]["name"]
                    )
                    new_amount = st.number_input("Сумма", value=transaction["amount"])

                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("Сохранить изменения")
                    with col2:
                        delete = st.form_submit_button("🗑 Удалить")

                    if submitted:
                        # Replace transaction immutably using tuple ops:
                        trans_tup = dicts_to_transactions(st.session_state["transactions"])
                        def _map_replace(t: Transaction):
                            if t.id != selected_trx_id:
                                return t
                            return Transaction(id=t.id, user_id=selected_user, acc_id=new_acc, cat_id=new_cat, amount=float(new_amount))
                        new_trans_tup = tuple(map(_map_replace, trans_tup))
                        st.session_state["transactions"] = models_to_dicts(new_trans_tup)
                        save_data_ui()
                        refresh_maps()
                        st.success("Транзакция обновлена")
                        st.rerun()

                    if delete:
                        trans_tup = dicts_to_transactions(st.session_state["transactions"])
                        new_trans_tup = tuple(filter(lambda t: t.id != selected_trx_id, trans_tup))
                        st.session_state["transactions"] = models_to_dicts(new_trans_tup)
                        save_data_ui()
                        refresh_maps()
                        st.success("Транзакция удалена")
                        st.rerun()

        # --- budgets ---
        with tabs[4]:
            st.subheader("Бюджеты")
            refresh_maps()
            user_budgets = filter_by_user(st.session_state["budgets"])
            budget_display = []
            for b in user_budgets:
                cat_name = st.session_state["categories_map"].get(b["cat_id"], {}).get("name", f"#{b['cat_id']}")
                budget_display.append({
                    "id": b["id"], "Категория": cat_name, "Лимит": fmt(b["limit"])
                })
            st.table(budget_display)

            # Optionally: allow updating budget limit in-place but immutably
            if user_budgets:
                st.subheader("Обновить лимит бюджета")
                bud_ids = [b["id"] for b in user_budgets]
                bid = st.selectbox("Выберите бюджет", bud_ids)
                current = next(b for b in user_budgets if b["id"] == bid)
                new_limit = st.number_input("Новый лимит", value=float(current["limit"]))
                if st.button("Обновить лимит"):
                    # Use pure update_budget
                    budgets_tup = dicts_to_budgets(st.session_state["budgets"])
                    new_budgets_tup = update_budget(budgets_tup, bid, float(new_limit))
                    st.session_state["budgets"] = models_to_dicts(new_budgets_tup)
                    save_data_ui()
                    refresh_maps()
                    st.success("Лимит обновлён")

# -------------------- Reports --------------------
elif menu == "Reports":
    st.title("📑 Reports")
    if not selected_user:
        st.warning("Выберите пользователя для отчётов.")
    else:
        trans_tup = dicts_to_transactions(st.session_state["transactions"])
        user_trx = [t for t in st.session_state["transactions"] if t.get("user_id") == selected_user]
        if not user_trx:
            st.warning("Нет транзакций для отчётов.")
        else:
            refresh_maps()
            income = sum(t["amount"] for t in user_trx if t["amount"] > 0)
            expense = sum(-t["amount"] for t in user_trx if t["amount"] < 0)
            balance = income - expense

            st.subheader("Общие показатели")
            col1, col2, col3 = st.columns(3)
            col1.metric("Доход", f"{fmt(income)} KZT")
            col2.metric("Расход", f"{fmt(expense)} KZT")
            col3.metric("Баланс", f"{fmt(balance)} KZT")

            st.subheader("По категориям")
            categories_map = {c["id"]: c for c in filter_by_user(st.session_state["categories"])}
            stats_cat = {}
            for t in trans_tup:
                if t.user_id != selected_user:
                    continue
                cat = categories_map.get(t.cat_id, {"name": "❓ Unknown"})
                cat_name = cat["name"]
                if cat_name not in stats_cat:
                    stats_cat[cat_name] = {"income": 0, "expense": 0}
                if t.amount > 0:
                    stats_cat[cat_name]["income"] += t.amount
                else:
                    stats_cat[cat_name]["expense"] += -t.amount

            st.table([
                {"Категория": name, "Доход": fmt(vals["income"]), "Расход": fmt(vals["expense"])}
                for name, vals in stats_cat.items()
            ])

            st.subheader("По подкатегориям")
            stats_subcat = {}
            for t in trans_tup:
                if t.user_id != selected_user:
                    continue
                cat = categories_map.get(t.cat_id, None)
                if not cat:
                    continue
                parent = categories_map.get(cat.get("parent_id"), None)
                key = f"{parent['name']} → {cat['name']}" if parent else cat["name"]
                if key not in stats_subcat:
                    stats_subcat[key] = {"income": 0, "expense": 0}
                if t.amount > 0:
                    stats_subcat[key]["income"] += t.amount
                else:
                    stats_subcat[key]["expense"] += -t.amount

            st.table([
                {"Категория/Подкатегория": name, "Доход": fmt(vals["income"]), "Расход": fmt(vals["expense"])}
                for name, vals in stats_subcat.items()
            ])

            user_budgets = filter_by_user(st.session_state["budgets"])
            if user_budgets:
                st.subheader("Бюджеты")
                budget_summary = []
                for b in user_budgets:
                    cat = categories_map.get(b["cat_id"], None)
                    if not cat:
                        continue
                    spent = sum(
                        -t["amount"] for t in st.session_state["transactions"]
                        if t["cat_id"] == b["cat_id"] and t["amount"] < 0 and t.get("user_id") == selected_user
                    )
                    budget_summary.append({
                        "Категория": cat["name"],
                        "Лимит": fmt(b["limit"]),
                        "Потрачено": fmt(spent),
                        "Остаток": fmt(b["limit"] - spent)
                    })
                st.table(budget_summary)


# -------------------- Settings --------------------
elif menu == "Settings":
    st.subheader("Soon")
    if st.button("Сбросить данные (очистить seed.json)"):
        st.session_state["users"] = []
        st.session_state["accounts"] = []
        st.session_state["categories"] = []
        st.session_state["transactions"] = []
        st.session_state["budgets"] = []
        save_data_ui()
        refresh_maps()
        st.success("Данные сброшены.")
