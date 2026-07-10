# database.py

import json
import os

from constants import DATABASE_FILE


def ensure_database():
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)

    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as f:
            json.dump([], f)


def load_items():
    ensure_database()

    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


def save_items(items):
    ensure_database()

    with open(DATABASE_FILE, "w") as f:
        json.dump(items, f, indent=4)


def add_item(item):
    items = load_items()
    items.append(item)
    save_items(items)


def remove_item(item_id):
    items = load_items()

    items = [item for item in items if item["id"] != item_id]

    save_items(items)


def update_item(item_id, updates):
    items = load_items()

    for item in items:
        if item["id"] == item_id:
            item.update(updates)
            break

    save_items(items)
