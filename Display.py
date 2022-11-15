import lcddriver
import time

display = lcddriver.lcd()

try:
    while True:
        print("Writing to display")
        display.lcd_display_string("lekker")