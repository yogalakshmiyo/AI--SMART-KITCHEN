from ultralytics import YOLO
import cv2

model=YOLO("yolov8n.pt")

FOOD_CLASSES=[ 
    "apple","banana","orange","broccoli","carrot",
    "hot dog","pizza","donut","cake","sandwich",
    "bottle","cup","bowl"
]


def detect_ingredients(image_path):
    results=model(image_path)
    detected=[]
    for result in results:
        for box in result.boxes:
            class_id   =int(box.cls[0])
            label      =model.names[class_id]
            confidence =float(box.conf[0])
            if label in FOOD_CLASSES and confidence>0.2:
                detected.append(label)
    return list(set(detected)) 
if __name__ =="__main__":
     print("AI Smart Kitchen - Starting...")
     print("Testing YOLO model...")
     test = detect_ingredients("test.jpg")
     print(f"Model working! Detected: {test}")
