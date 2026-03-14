# Built-in recipe database - no API needed!
RECIPES = {
    "apple": [
        {"title": "Apple Salad",
         "ingredients": ["apple", "banana"],
         "instructions": "Slice apple and banana. Mix together. Serve fresh!"},
        {"title": "Apple Juice",
         "ingredients": ["apple"],
         "instructions": "Blend apple with water. Strain and serve cold!"},
    ],
    "banana": [
        {"title": "Banana Smoothie",
         "ingredients": ["banana"],
         "instructions": "Blend banana with milk. Add honey. Serve cold!"},
        {"title": "Banana Salad",
         "ingredients": ["banana", "orange"],
         "instructions": "Slice banana and orange. Mix and serve!"},
    ],
    "carrot": [
        {"title": "Carrot Soup",
         "ingredients": ["carrot"],
         "instructions": "Boil carrots. Blend smooth. Add salt and pepper!"},
        {"title": "Carrot Salad",
         "ingredients": ["carrot", "orange"],
         "instructions": "Grate carrot. Add orange juice. Mix well!"},
    ],
    "cake": [
        {"title": "Cake with Fruits",
         "ingredients": ["cake", "apple", "banana"],
         "instructions": "Place cake on plate. Top with sliced fruits!"},
    ],
    "pizza": [
        {"title": "Veggie Pizza",
         "ingredients": ["pizza", "broccoli", "carrot"],
         "instructions": "Top pizza with veggies. Bake at 180C for 15 mins!"},
    ],
    "broccoli": [
        {"title": "Stir Fry",
         "ingredients": ["broccoli", "carrot"],
         "instructions": "Stir fry broccoli and carrot. Add soy sauce!"},
    ],
}

def suggest_recipes(ingredients: list):
    print("\n" + "="*50)
    print("🍽️  RECIPE SUGGESTIONS")
    print("="*50)

    if not ingredients:
        print("❌ No ingredients detected!")
        return []

    found_recipes = []
    for ing in ingredients:
        if ing in RECIPES:
            for recipe in RECIPES[ing]:
                if recipe not in found_recipes:
                    found_recipes.append(recipe)

    if not found_recipes:
        print(f"❌ No recipes found for: {ingredients}")
        print("💡 Try with: apple, banana, carrot, broccoli")
        return []

    for i, recipe in enumerate(found_recipes[:5], 1):
        have    = [x for x in recipe["ingredients"]
                   if x in ingredients]
        missing = [x for x in recipe["ingredients"]
                   if x not in ingredients]

        print(f"\n{i}. 🍳 {recipe['title']}")
        print(f"   ✅ Have:    {', '.join(have) if have else 'none'}")
        print(f"   ❌ Missing: {', '.join(missing) if missing else 'none'}")
        print(f"   📝 How to: {recipe['instructions']}")

    return found_recipes

if __name__ == "__main__":
    suggest_recipes(["apple", "banana", "cake"])