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


# Get digit from rotary dial
def rotary():
    flag = False
    counter = 0
    false_flag_tick = 0
    while True:
        sleep(0.001)
        new_flag = (GPIO.input(21) == 1)
        if flag != new_flag:
            counter += 1
            flag = new_flag
        if not flag and counter >= 2:
            false_flag_tick += 1
        else:
            false_flag_tick = 0

        if false_flag_tick > 100:
            ctr = int(counter / 2) - 1
            if ctr >= 0:
                result = str(ctr)
                print(result)
                return result
            else
                break
        
    return None


def update_lcd_until_enter(lcd, msg, scroll=False):
    print("upd_lcd")
    lcd.blink(True)
    result = ""
    lcd.clear()
    lcd.message(msg.format(result))
    while True:
        ch = rotary()
        if ch == '\r':
            lcd.blink(False)
            return (result, True)
        elif ch == 27:
            break
        elif ch:
            result = result + ch
            lcd.message(ch)

            

    lcd.blink(False)
    return (result, False)


# Start GSM modem
def start_modem():
    print "Starting modem..."
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(16, GPIO.LOW)

