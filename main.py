import time
import getpass
import cv2
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

from config import (
    LCD_ADDRESS, LCD_COLS, LCD_ROWS,
    LED_PIN, BUZZER_PIN,
    PASSWORD, FACE_ID, FACE_THRESHOLD, MODEL_FILE
)

# -----------------------------
# CAMERA
# -----------------------------
try:
    from picamera2 import Picamera2
except ImportError:
    raise SystemExit(
        "Picamera2 is not installed. Run: "
        "sudo apt install -y python3-picamera2"
    )

# -----------------------------
# OPENCV FACE MODULE
# -----------------------------
if not hasattr(cv2, "face"):
    raise SystemExit(
        "Your OpenCV build does not contain cv2.face."
    )

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_FILE)

# -----------------------------
# FACE CASCADE
# -----------------------------
CASCADE = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(CASCADE)

# FIX: use face_detector, not detector
if face_detector.empty():
    raise SystemExit(
        "ERROR: Face cascade could not be loaded."
    )

# -----------------------------
# LCD
# -----------------------------
lcd = CharLCD(
    'PCF8574',
    LCD_ADDRESS,
    cols=LCD_COLS,
    rows=LCD_ROWS
)

# -----------------------------
# GPIO
# -----------------------------
GPIO.setmode(GPIO.BCM)

GPIO.setup(
    LED_PIN,
    GPIO.OUT,
    initial=GPIO.LOW
)

GPIO.setup(
    BUZZER_PIN,
    GPIO.OUT,
    initial=GPIO.LOW
)


# -----------------------------
# LCD FUNCTION
# -----------------------------
def lcd_message(line1, line2=""):

    lcd.clear()

    lcd.write_string(
        line1[:LCD_COLS]
    )

    lcd.crlf()

    lcd.write_string(
        line2[:LCD_COLS]
    )


# -----------------------------
# BUZZER FUNCTION
# -----------------------------
def beep(duration=0.15, times=1, gap=0.12):

    for _ in range(times):

        GPIO.output(
            BUZZER_PIN,
            GPIO.HIGH
        )

        time.sleep(duration)

        GPIO.output(
            BUZZER_PIN,
            GPIO.LOW
        )

        time.sleep(gap)


# -----------------------------
# FACE VERIFICATION
# -----------------------------
def check_face():

    lcd_message(
        "Scanning face...",
        "Look at camera"
    )

    print("\nSTEP 1: CAMERA / FACE SCAN")
    print("Look at the camera...")

    picam2 = Picamera2()

    picam2.configure(
        picam2.create_preview_configuration(
            main={
                "format": "RGB888",
                "size": (640, 480)
            }
        )
    )

    picam2.start()

    time.sleep(1)

    verified = False

    start = time.time()

    try:

        while time.time() - start < 10:

            frame = picam2.capture_array()

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_RGB2GRAY
            )

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5
            )

            for (x, y, w, h) in faces:

                face_id, confidence = recognizer.predict(
                    gray[y:y+h, x:x+w]
                )

                print(
                    "Detected ID:",
                    face_id,
                    "Confidence:",
                    round(confidence, 2)
                )

                if (
                    face_id == FACE_ID
                    and confidence < FACE_THRESHOLD
                ):

                    verified = True

                    print("FACE VERIFIED")

                    print(
                        "Confidence distance:",
                        round(confidence, 2)
                    )

                    break

            if verified:
                break

            # Draw detected face
            for (x, y, w, h) in faces:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

            cv2.imshow(
                "Smart Access Camera - Press Q",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        picam2.stop()

        cv2.destroyAllWindows()

    # -----------------------------
    # FACE SUCCESS
    # -----------------------------
    if verified:

        lcd_message(
            "FACE VERIFIED",
            "Enter password"
        )

        return True

    # -----------------------------
    # FACE FAILURE
    # -----------------------------
    lcd_message(
        "ACCESS DENIED",
        "Unknown face"
    )

    beep(
        duration=0.25,
        times=2
    )

    print(
        "ACCESS DENIED - Face not recognized"
    )

    time.sleep(2)

    return False


# -----------------------------
# PASSWORD VERIFICATION
# -----------------------------
def check_password():

    print(
        "\nSTEP 2: PASSWORD VERIFICATION"
    )

    lcd_message(
        "PASSWORD",
        "Check terminal"
    )

    entered = getpass.getpass(
        "Enter password: "
    )

    if entered == PASSWORD:

        print("PASSWORD VERIFIED")

        return True

    print(
        "ACCESS DENIED - Incorrect password"
    )

    lcd_message(
        "ACCESS DENIED",
        "Wrong password"
    )

    beep(
        duration=0.25,
        times=2
    )

    time.sleep(2)

    return False


# -----------------------------
# ACCESS GRANTED
# -----------------------------
def access_granted():

    print(
        "\nBOTH FACTORS VERIFIED"
    )

    print(
        "ACCESS GRANTED"
    )

    lcd_message(
        "ACCESS GRANTED",
        "Welcome!"
    )

    # LED ON
    GPIO.output(
        LED_PIN,
        GPIO.HIGH
    )

    # Success beep
    beep(
        duration=0.15,
        times=2
    )

    # Keep access indicator ON
    # for 5 seconds
    time.sleep(5)

    # LED OFF
    GPIO.output(
        LED_PIN,
        GPIO.LOW
    )

    lcd_message(
        "SYSTEM READY",
        "Scan face"
    )

    print(
        "Access indicator OFF"
    )


# -----------------------------
# COMPLETE AUTHENTICATION
# -----------------------------
def authenticate():

    # FIRST FACTOR
    if not check_face():

        return

    print(
        "First factor passed."
    )

    print(
        "Now verify password."
    )

    # SECOND FACTOR
    if not check_password():

        return

    # BOTH FACTORS PASSED
    access_granted()


# -----------------------------
# MAIN PROGRAM
# -----------------------------
try:

    lcd_message(
        "SMART ACCESS",
        "System Ready"
    )

    while True:

        print(
            "\n=============================="
        )

        print(
            " TWO-FACTOR SMART ACCESS"
        )

        print(
            "=============================="
        )

        print(
            "1. Authenticate"
        )

        print(
            "2. Quit"
        )

        choice = input(
            "Choose: "
        ).strip()

        if choice == "1":

            authenticate()

        elif choice == "2":

            break

        else:

            print(
                "Invalid choice"
            )

            lcd_message(
                "INVALID OPTION",
                "Try again"
            )

            time.sleep(1)

finally:

    GPIO.output(
        LED_PIN,
        GPIO.LOW
    )

    GPIO.output(
        BUZZER_PIN,
        GPIO.LOW
    )

    lcd.clear()

    lcd.close()

    GPIO.cleanup()
