import sys
import tty
import termios
import serial
import RPi.GPIO as GPIO      
import os
import Adafruit_CharLCD as LCD
import subprocess
from subprocess import *
from time import sleep, strftime
from datetime import datetime

# Read single character without waiting for enter
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Find a suitable character in a text or string and get its position
def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i


# Get digit from rotary dial
def rotary():
    flag=False
    counter=0
    false_flag_tick=0
    while True:
        sleep(0.001)
        new_flag=(GPIO.input(21)==1)
        if flag != new_flag:
            counter += 1
            flag=new_flag
        if not flag and counter >= 2:
            false_flag_tick += 1
        else:
            false_flag_tick = 0

        if false_flag_tick > 100 and counter >= 2:
            result = str(counter/2 - 1)
            print(result)
            return result
    return "0"

def update_lcd_until_enter(lcd, msg, scroll=False):
    print("upd_lcd")
    lcd.blink(True)
    result = ""
    lcd.clear()
    lcd.message(msg.format(result))
    while (True):
        ch = rotary() #getch()
        if ch == '\r':
            lcd.blink(False)
            return (result, True)
        elif ch == 27:
            break
        result = result + ch
        if not scroll:
            lcd.message(ch)
        else:
            if len(result) < 16:
                lcd.message(ch)
            else:
                lcd.clear()
                lcd.message(msg.format(result[(len(result)-16):])) 
    lcd.blink(False)
    return (result, False)

# Start GSM modem
def start_modem():
    print "Starting modem..."
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(16, GPIO.LOW)

