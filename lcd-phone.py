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
from engine import getch, find, rotary, update_lcd_until_enter, start_modem

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

# GPIO, serial, modem and LCD setup
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Rotary
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Hook
GPIO.setup(20, GPIO.OUT)  # Ringer
GPIO.output(20, GPIO.LOW)
start_modem()


def hook_lifted():
    return (GPIO.input(26) != 0)


def call():
    False


def init_call(number):
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
    lcd.message("Preparing...")
    status = init_call(number)
    if not status:
        return
    lcd.message("Calling...")
    status = call()
    if not status:
        return

# --- --- --- --- --- --- --- --- --- --- --- ---


# Main loop
def main():
    # ringer(1)
    while True:
        print("Main loop")
        sleep(0.5)
        if hook_lifted():
            gui_call()

        # recv_call()

        lcd.clear()
        sleep(0.5)
        lcd.message("Ready")


if __name__ == "__main__":
    main()
