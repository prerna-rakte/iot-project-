#!/bin/bash
set -e

echo "Installing system packages..."
sudo apt update
sudo apt install -y python3-pip python3-opencv python3-numpy python3-pil python3-smbus i2c-tools python3-picamera2

echo "Installing RPLCD..."
if pip3 install RPLCD; then
    echo "RPLCD installed."
else
    pip3 install --break-system-packages RPLCD
fi

echo ""
echo "Installation complete."
echo "Enable I2C with: sudo raspi-config"
echo "Then test the LCD with: sudo i2cdetect -y 1"
