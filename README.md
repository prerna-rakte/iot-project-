# Two-Factor Camera + Password Smart Access System

Modified Practical 15 for Raspberry Pi 4 (64-bit).

## Hardware
- Raspberry Pi 4 Model B
- CSI camera
- 16x2 I2C LCD with PCF8574 backpack
- Green LED + 220 ohm resistor
- Active buzzer

No relay or physical door lock is used.

## GPIO wiring
LCD:
- VCC -> Pin 2 (5V)
- GND -> Pin 6 (GND)
- SDA -> Pin 3 (GPIO2)
- SCL -> Pin 5 (GPIO3)

Green LED:
- GPIO17 / Pin 11 -> 220 ohm resistor -> LED anode (+)
- LED cathode (-) -> GND (Pin 14)

Buzzer module:
- IN/S -> GPIO27 / Pin 13
- VCC -> 5V / Pin 4
- GND -> GND / Pin 14

## Software
Install:
sudo apt update
sudo apt install -y python3-pip python3-opencv python3-numpy python3-pil python3-smbus i2c-tools
pip3 install RPLCD

Enable I2C:
sudo raspi-config

Then Interface Options -> I2C -> Enable.

Check LCD:
sudo i2cdetect -y 1

Typical address: 0x27. Change LCD_ADDRESS in config.py if yours differs.

Check CSI camera:
libcamera-hello --list-cameras
libcamera-hello

## Project workflow
1. Test LCD: python3 lcd_test.py
2. Test LED: python3 led_test.py
3. Test buzzer: python3 buzzer_test.py
4. Capture face samples: python3 enroll_face.py
5. Train model: python3 train_face.py
6. Run final system: python3 main.py

## Important
The final program uses the Raspberry Pi camera stack through Picamera2. If Picamera2 is not installed on your Raspberry Pi OS image, install it using:
sudo apt install -y python3-picamera2

The face recognizer requires an OpenCV build containing cv2.face.LBPHFaceRecognizer_create().
Check:
python3 -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'face'))"

If the result is False, do not randomly install multiple OpenCV versions; fix the OpenCV installation first.

The default demonstration password is Door@123. Change it in config.py before presentation.
