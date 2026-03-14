# Simple nutrition database - no API needed!
NUTRITION_DB = {
    "apple":    {"calories": 95,  "protein": 0.5, "carbs": 25, "fat": 0.3},
    "banana":   {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4},
    "orange":   {"calories": 62,  "protein": 1.2, "carbs": 15, "fat": 0.2},
    "broccoli": {"calories": 55,  "protein": 3.7, "carbs": 11, "fat": 0.6},
    "carrot":   {"calories": 41,  "protein": 0.9, "carbs": 10, "fat": 0.2},
    "cake":     {"calories": 257, "protein": 3.2, "carbs": 36, "fat": 11},
    "pizza":    {"calories": 285, "protein": 12,  "carbs": 36, "fat": 10},
    "sandwich": {"calories": 200, "protein": 8,   "carbs": 28, "fat": 6},
    "donut":    {"calories": 253, "protein": 4,   "carbs": 30, "fat": 14},
    "hot dog":  {"calories": 180, "protein": 7,   "carbs": 16, "fat": 10},
    "bottle":   {"calories": 0,   "protein": 0,   "carbs": 0,  "fat": 0},
    "bowl":     {"calories": 0,   "protein": 0,   "carbs": 0,  "fat": 0},
}

def get_nutrition(ingredients: list):
    print("\n" + "="*45)
    print("🥗 NUTRITION ESTIMATION")
    print("="*45)
    print(f"{'Item':<15} {'Cal':>6} {'Protein':>8} {'Carbs':>7} {'Fat':>6}")
    print("-"*45)

    total_cal     = 0
    total_protein = 0
    total_carbs   = 0
    total_fat     = 0
    nutrition_list = []

    for item in ingredients:
        if item in NUTRITION_DB:
            n = NUTRITION_DB[item]
            print(f"{item:<15} {n['calories']:>6} "
                  f"{n['protein']:>7}g "
                  f"{n['carbs']:>6}g "
                  f"{n['fat']:>5}g")
            total_cal     += n['calories']
            total_protein += n['protein']
            total_carbs   += n['carbs']
            total_fat     += n['fat']
            nutrition_list.append({"name": item, **n})

    print("-"*45)
    print(f"{'TOTAL':<15} {total_cal:>6} "
          f"{total_protein:>7}g "
          f"{total_carbs:>6}g "
          f"{total_fat:>5}g")
    print(f"\n🔥 Total Calories: {total_cal} kcal")

    if total_cal < 300:
        print("✅ Low calorie meal!")
    elif total_cal < 600:
        print("⚠️  Medium calorie meal")
    else:
        print("❌ High calorie meal!")

    return nutrition_list, total_cal

if __name__ == "__main__":
    get_nutrition(["apple", "cake", "banana"])