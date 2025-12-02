from typing import Callable, Dict, List
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Event:
    name: str
    ts: str
    payload: dict

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event, dict], dict]]] = defaultdict(list)

    def subscribe(self, name: str, handler: Callable[[Event, dict], dict]):
        self._subscribers[name].append(handler)

    def publish(self, name: str, payload: dict):
        event = Event(name, datetime.now().isoformat(), payload)
        results = []
        for handler in self._subscribers.get(name, []):
            results.append(handler(event, payload))
        return results

# ---- Подписчики ----
def update_balance(event, state: dict):
    acc_id = event.payload.get("account_id")
    amount = event.payload.get("amount", 0)
    new_state = state.copy()
    # Не добавляем payload, только агрегат
    new_state[acc_id] = new_state.get(acc_id, 0) + amount
    return {acc_id: new_state[acc_id]}

def check_budget(event, state: dict):
    cat_id = event.payload.get("cat_id")
    amount = event.payload.get("amount", 0)
    new_state = state.copy()
    new_state[cat_id] = new_state.get(cat_id, 0) + amount
    return {cat_id: new_state[cat_id]}

def create_alert(event, state: dict):
    alerts = state.get("alerts", [])
    alerts = alerts + [f"{event.name} triggered for {event.payload}"]
    return {"alerts": alerts}
