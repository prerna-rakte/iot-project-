import os
import cv2
import numpy as np
from PIL import Image
from config import DATASET_DIR, MODEL_FILE

if not hasattr(cv2, "face"):
    raise SystemExit(
        "Your OpenCV build does not contain cv2.face. "
        "Install/use an OpenCV contrib build that provides LBPHFaceRecognizer."
    )

recognizer = cv2.face.LBPHFaceRecognizer_create()
CASCADE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"

detector = cv2.CascadeClassifier(CASCADE)

if detector.empty():
    raise SystemExit("ERROR: Face cascade could not be loaded.")


face_samples = []
ids = []

for filename in os.listdir(DATASET_DIR):
    if not filename.lower().endswith(".jpg"):
        continue

    path = os.path.join(DATASET_DIR, filename)
    pil_img = Image.open(path).convert("L")
    img_numpy = np.array(pil_img, "uint8")

    try:
        face_id = int(filename.split(".")[1])
    except (IndexError, ValueError):
        continue

    faces = detector.detectMultiScale(img_numpy)

    for (x, y, w, h) in faces:
        face_samples.append(img_numpy[y:y+h, x:x+w])
        ids.append(face_id)

if not face_samples:
    raise SystemExit(
        "No usable face samples found. Run enroll_face.py first."
    )

print("Training face recognizer...")
recognizer.train(face_samples, np.array(ids))
recognizer.write(MODEL_FILE)

print("Training completed.")
print("Saved model:", MODEL_FILE)
print("Images used:", len(face_samples))
