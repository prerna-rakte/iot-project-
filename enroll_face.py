import os
import cv2
import time
from config import DATASET_DIR, FACE_ID, FACE_SAMPLES

os.makedirs(DATASET_DIR, exist_ok=True)

# Raspberry Pi CSI camera support
try:
    from picamera2 import Picamera2
except ImportError:
    raise SystemExit(
        "Picamera2 is not installed. Run: sudo apt install -y python3-picamera2"
    )
CASCADE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"

detector = cv2.CascadeClassifier(CASCADE)

if detector.empty():
    raise SystemExit("ERROR: Face cascade could not be loaded.")



picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))
picam2.start()
time.sleep(2)

count = 0
print("FACE ENROLLMENT")
print("Look at the camera. Press Q to stop.")

try:
    while count < FACE_SAMPLES:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            count += 1
            filename = os.path.join(
                DATASET_DIR, "User.{}.{}.jpg".format(FACE_ID, count)
            )
            cv2.imwrite(filename, gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                frame, "Sample {}".format(count),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0), 2
            )
            break

        cv2.imshow("Face Enrollment - Press Q", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()

print("Face enrollment completed.")
print("Images saved:", count)
