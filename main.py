from kitchen_detection  import detect_ingredients
from nutrition          import get_nutrition
from inventory          import check_expiry, add_item, get_available_ingredients
from recipe_suggester   import suggest_recipes

def run_from_image(image_path: str):
    print("\n" + "🍳"*20)
    print("   AI SMART KITCHEN - FULL ANALYSIS")
    print("🍳"*20)

    # STEP 1 - Detect
    print("\n📷 STEP 1: Scanning image...")
    ingredients = detect_ingredients(image_path)
    if ingredients:
        print(f"✅ Detected: {ingredients}")
    else:
        print("❌ Nothing detected - try another image!")
        return

    # STEP 2 - Nutrition
    print("\n🥗 STEP 2: Calculating nutrition...")
    get_nutrition(ingredients)

    # STEP 3 - Recipes
    print("\n🍽️  STEP 3: Finding recipes...")
    suggest_recipes(ingredients)

    # STEP 4 - Inventory
    print("\n📦 STEP 4: Checking inventory...")
    warnings = check_expiry()
    if warnings:
        print("\n⚠️  EXPIRY WARNINGS:")
        for w in warnings:
            print(f"   🔔 {w}")

def setup_sample_inventory():
    print("📦 Setting up sample inventory...")
    add_item("apple",    5, "2026-03-20")
    add_item("banana",   3, "2026-03-16")
    add_item("carrot",   8, "2026-03-25")
    add_item("milk",     2, "2026-03-14")
    add_item("broccoli", 4, "2026-03-18")

if __name__ == "__main__":
    print("\n" + "="*40)
    print("  🍳 AI SMART KITCHEN")
    print("="*40)
    print("1. Scan image")
    print("2. Check inventory")
    print("3. Setup sample inventory")
    print("4. Suggest recipes from inventory")

    choice = input("\nChoose (1/2/3/4): ")

    if choice == "1":
        path = input("Image path (or press Enter for test.jpg): ")
        if not path:
            path = "test.jpg"
        run_from_image(path)

    elif choice == "2":
        check_expiry()

    elif choice == "3":
        setup_sample_inventory()
        print("✅ Sample inventory created!")

    elif choice == "4":
        available = get_available_ingredients()
        print(f"\n✅ Available: {available}")
        suggest_recipes(available)