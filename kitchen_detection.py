from google import genai
from google.genai import types
import PIL.Image
import os

GEMINI_API_KEY = os.environ.get(
    'GEMINI_API_KEY',
    'AIzaSyDsGlirmdbDL82qLPywe_X4mcB6H7h'
)

client = genai.Client(api_key=GEMINI_API_KEY)

def detect_ingredients(image_path: str):
    try:
        img = PIL.Image.open(image_path).convert('RGB')

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                "List all food items you see in this image. "
                "Write only the food names separated by commas. "
                "Example: potato, tomato, onion. "
                "Just food names, nothing else.",
                img
            ]
        )

        text = response.text.strip()
        print(f"Gemini: {text}")

        items = [i.strip().lower() for i in text.split(',')]
        items = [i for i in items if 1 < len(i) < 30]
        bad = ['the','a','an','and','or','with','some','fresh',
               'raw','cooked','food','item','image','photo',
               'picture','see','shows','here','are','is','i']
        items = [i for i in items if i not in bad]

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