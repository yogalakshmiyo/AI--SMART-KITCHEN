import google.generativeai as genai
import PIL.Image
import os
import json

GEMINI_API_KEY = "AIzaSyDsGlirmdbDL82qLPywe_X4mcB6H7h"
genai.configure(api_key=GEMINI_API_KEY)

def detect_ingredients(image_path: str):
    try:
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """Look at this image. List ALL food items you see.
Return ONLY a JSON array like: ["apple", "banana", "rice"]
If no food found return: []
Return ONLY the JSON array, nothing else."""
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        if '```' in text:
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        text = text.strip()
        ingredients = json.loads(text)
        ingredients = [i.lower().strip() for i in ingredients]
        print(f"Gemini Detected: {ingredients}")
        return ingredients[:15]
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
                confidence = float(box.conf[0])
                if confidence > 0.2:
                    detected.append(label)
        return list(set(detected))
    except:
        return []

if __name__ == "__main__":
    items = detect_ingredients("test.jpg")
    print(f"Detected: {items}")