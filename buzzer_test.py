import RPi.GPIO as GPIO
import time
from config import BUZZER_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    print('Buzzer ON')
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
finally:
    GPIO.cleanup()
