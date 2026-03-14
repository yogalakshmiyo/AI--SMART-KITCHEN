import json, os
from datetime import datetime, date

INVENTORY_FILE = "inventory.json"

MIN_QUANTITIES = {
    "apple":    3,
    "banana":   4,
    "milk":     2,
    "carrot":   5,
    "tomato":   4,
    "onion":    5,
    "potato":   5,
    "egg":     10,
    "bread":    1,
    "broccoli": 3,
    "orange":   4,
}

def generate_shopping_list(detected=[]):
    shopping = []
    today    = date.today()

    inventory = {}
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as f:
            inventory = json.load(f)

    # Check minimum stock
    for item, min_qty in MIN_QUANTITIES.items():
        if item not in inventory:
            shopping.append({
                "item":     item.capitalize(),
                "reason":   "Not in stock",
                "priority": "🔴 High",
                "qty":      min_qty
            })
        else:
            info      = inventory[item]
            expiry    = datetime.strptime(
                            info["expiry_date"], "%Y-%m-%d").date()
            days_left = (expiry - today).days
            qty       = info["quantity"]

            if days_left < 0:
                shopping.append({
                    "item":     item.capitalize(),
                    "reason":   "Expired!",
                    "priority": "🔴 High",
                    "qty":      min_qty
                })
            elif days_left <= 2:
                shopping.append({
                    "item":     item.capitalize(),
                    "reason":   f"Expires in {days_left} days",
                    "priority": "🟡 Medium",
                    "qty":      min_qty
                })
            elif qty < min_qty:
                shopping.append({
                    "item":     item.capitalize(),
                    "reason":   f"Low stock ({qty})",
                    "priority": "🟡 Medium",
                    "qty":      min_qty - qty
                })

    # Add missing detected ingredients
    for ing in detected:
        if ing not in inventory:
            shopping.append({
                "item":     ing.capitalize(),
                "reason":   "Needed for recipe",
                "priority": "🟢 Low",
                "qty":      2
            })

    if not shopping:
        print("✅ Kitchen fully stocked!")
        return []

    # Save to file
    with open("shopping_list.txt", "w", encoding="utf-8") as f:
        f.write("🛒 SHOPPING LIST\n")
        f.write("="*40 + "\n")
        for s in shopping:
            f.write(f"{s['priority']} {s['item']:15} "
                   f"Qty:{s['qty']}  ({s['reason']})\n")

    # Print
    print("\n🛒 SHOPPING LIST")
    print("="*40)
    for s in shopping:
        print(f"{s['priority']} {s['item']:15} "
              f"Qty:{s['qty']:3}  ({s['reason']})")
    print(f"\n✅ Saved to shopping_list.txt")
    return shopping

if __name__ == "__main__":
    generate_shopping_list()