from RPLCD.i2c import CharLCD
from config import LCD_ADDRESS, LCD_COLS, LCD_ROWS
import time

lcd = CharLCD('PCF8574', LCD_ADDRESS, cols=LCD_COLS, rows=LCD_ROWS)

try:
    lcd.clear()
    lcd.write_string('Smart Access')
    lcd.crlf()
    lcd.write_string('System Ready')
    time.sleep(3)

    lcd.clear()
    lcd.write_string('LCD TEST OK')
    time.sleep(2)
finally:
    lcd.clear()
    lcd.close()
