import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def announce_ingredients(ingredients):
    if not ingredients:
        speak("No ingredients detected.")
        return
    text = f"I detected {len(ingredients)} ingredients. They are: "
    text += ", ".join(ingredients)
    speak(text)

def announce_recipes(recipes):
    if not recipes:
        speak("Sorry, no recipes found.")
        return
    speak(f"I found {len(recipes)} recipes for you!")
    for i, r in enumerate(recipes[:3], 1):
        speak(f"Recipe {i}: {r['title']}")

def announce_calories(total):
    speak(f"Total estimated calories is {total} kilocalories.")

def announce_expiry(item, days):
    if days < 0:
        speak(f"Warning! {item} has already expired!")
    elif days <= 3:
        speak(f"Alert! {item} will expire in {days} days!")

if __name__ == "__main__":
    speak("Welcome to AI Smart Kitchen!")
    announce_ingredients(["apple", "banana", "cake"])
    announce_calories(457)