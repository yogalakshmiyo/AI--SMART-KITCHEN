import json, os
from datetime import datetime, date

INVENTORY_FILE = "inventory.json"

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return {}
    with open(INVENTORY_FILE, "r") as f:
        return json.load(f)

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=2)

def add_item(name: str, quantity: int, expiry_date: str):
    inventory = load_inventory()
    inventory[name] = {
        "quantity": quantity,
        "expiry_date": expiry_date,
        "added_on": str(date.today())
    }
    save_inventory(inventory)
    print(f"✅ Added: {name} (qty:{quantity}, expires:{expiry_date})")

def check_expiry():
    inventory = load_inventory()
    if not inventory:
        print("📦 Inventory is empty! Add items first.")
        return []

    today     = date.today()
    warnings  = []

    print("\n" + "="*50)
    print("📦 INVENTORY STATUS")
    print("="*50)
    print(f"{'Item':<15} {'Qty':>4} {'Expiry':>12} {'Status'}")
    print("-"*50)

    for name, info in inventory.items():
        expiry    = datetime.strptime(
                        info["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry - today).days
        qty       = info["quantity"]

        if days_left < 0:
            status = "❌ EXPIRED"
            warnings.append(f"{name} EXPIRED!")
        elif days_left <= 2:
            status = f"🔴 {days_left}d left"
            warnings.append(f"{name} expires in {days_left} days!")
        elif days_left <= 5:
            status = f"🟡 {days_left}d left"
        else:
            status = f"✅ {days_left}d left"

        print(f"{name:<15} {qty:>4} "
              f"{info['expiry_date']:>12}  {status}")

    print("="*50)
    return warnings

def get_available_ingredients():
    inventory = load_inventory()
    today     = date.today()
    available = []
    for name, info in inventory.items():
        expiry    = datetime.strptime(
                        info["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry - today).days
        if days_left >= 0 and info["quantity"] > 0:
            available.append(name)
    return available

if __name__ == "__main__":
    # Add sample items
    add_item("apple",   5, "2026-03-20")
    add_item("banana",  3, "2026-03-15")
    add_item("milk",    2, "2026-03-14")
    add_item("carrot",  8, "2026-03-25")
    add_item("cake",    1, "2026-03-13")
    check_expiry()