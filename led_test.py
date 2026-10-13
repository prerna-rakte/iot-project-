import RPi.GPIO as GPIO
import time
from config import LED_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    print('LED ON for 5 seconds')
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(LED_PIN, GPIO.LOW)
finally:
    GPIO.cleanup()
