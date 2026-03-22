import google.generativeai as genai
import PIL.Image
import os, json, re

GEMINI_API_KEY = os.environ.get(
    'GEMINI_API_KEY',
    'AIzaSyDsGlirmdbDL82qLPywe_X4mcB6H7h'
)
genai.configure(api_key=GEMINI_API_KEY)

def detect_ingredients(image_path: str):
    try:
        img = PIL.Image.open(image_path).convert('RGB')
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = """What food items do you see in this image?
List each food item separated by commas.
Example: potato, tomato, onion, rice
Just list the foods, nothing else."""

        response = model.generate_content([prompt, img])
        text = response.text.strip()
        print(f"Gemini said: {text}")

        # Parse comma-separated response
        items = [i.strip().lower() for i in text.split(',')]
        items = [i for i in items if len(i) > 1 and len(i) < 30]
        # Remove non-food words
        bad_words = ['the','a','an','and','or','with','some',
                     'fresh','raw','cooked','food','item','image',
                     'photo','picture','see','shows']
        items = [i for i in items if i not in bad_words]
        
        print(f"✅ Detected: {items[:10]}")
        return items[:10]

    except Exception as e:
        print(f"Gemini Error: {e}")
        return yolo_detect(image_path)

def yolo_detect(image_path: str):
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")
        results = model(image_path)
        detected = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                if float(box.conf[0]) > 0.2:
                    detected.append(label)
        return list(set(detected))
    except:
        return []

if __name__ == "__main__":
    print(detect_ingredients("test.jpg"))