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

# Raspberry Pi pin configuration:
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2


# Start GSM modem
def start_modem():
    print "Starting modem..."
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(16, GPIO.LOW)


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
        if not flag:
            false_flag_tick += 1
        else:
            false_flag_tick = 0

        if false_flag_tick > 100:
            ctr = int(counter / 2) - 1
            if ctr >= 0:
                result = str(ctr)
                print(result)
                return result
            else:
                break
        
    return None


def update_lcd_until_enter(lcd, msg):
    print("upd_lcd")
    lcd.blink(True)
    result = ""
    lcd.clear()
    lcd.message(msg.format(result))
    while hook_lifted():
        ch = rotary()
        if ch == '\r':
            lcd.blink(False)
            return (result, True)
        elif ch:
            result = result + ch
            lcd.message(ch)
        elif len(result) >= 10:
            break

    lcd.blink(False)
    return (result, True)


def hook_lifted():
    return (GPIO.input(26) != 0)


def call(number):
    print('init_call')
    port.write('AT\r\n')
    rcv = port.read(10)
    print(rcv)

    port.write('ATD' + number + ' \r\n')
    rcv = port.read(10)
    print(rcv)

    while hook_lifted():
        sleep(0.1)

    True


def recv_call():
    print('recv_call')
    sleep(0.5)
    port.write('ATA\r\n')
    sleep(0.5)
    rcv = port.read(10)
    print(rcv)
    sleep(0.5)
    True


def ringer(time):
    GPIO.output(20, GPIO.HIGH)
    sleep(time)
    GPIO.output(20, GPIO.LOW)


def gui_call():
    print("gui_call")
    (number, status) = update_lcd_until_enter(lcd, "Enter number:\n{0}")
    if not status:
        return
    sleep(0.5)
    lcd.clear()
    sleep(0.5)
    lcd.message("Calling...")
    status = call(number)
    print(status)

# --- --- --- --- --- --- --- --- --- --- --- ---

# GPIO, serial, modem and LCD setup
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Rotary
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Hook
GPIO.setup(20, GPIO.OUT)  # Ringer
GPIO.output(20, GPIO.LOW)
start_modem()

# Main loop
while True:
    print("Main loop")
    sleep(0.5)
    if hook_lifted():
        gui_call()

    # recv_call()

    lcd.clear()
    sleep(0.5)
    lcd.message("Ready")
