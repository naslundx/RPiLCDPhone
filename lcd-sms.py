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
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4
lcd_columns   = 16
lcd_rows      = 2

# GPIO, serial, modem and LCD setup
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
start_modem()

# Rotary setup
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize send SMS
def init_send_sms():
    print("init_send_sms")
    # Prepare
    port.write('AT\r\n')
    rcv = port.read(10)
    print(rcv)
    #if not 'OK' in rcv:
    #    return False
    sleep(1)
    
    # Disable the Echo
    port.write('ATE0\r\n')      
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return False
    sleep(1)
    
    # Select Message format as Text mode 
    port.write('AT+CMGF=1\r\n')  
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return False
    sleep(1)
    
    # New SMS Message Indications
    port.write('AT+CNMI=2,1,0,0,0\r\n')   
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return False
    sleep(1)
    print("Send SMS Initialized.")
    return True


def send_sms(number, message):
    print('send_sms')
    # Pass on recepient number
    port.write('AT+CMGS="%s"\r\n' % number)
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return False
    sleep(1)
    
    # Pass on message
    port.write('%s\r\n' % message)
    rcv = port.read(10)
    print("!"+rcv)
    
    # Send
    port.write("\x1A")
    for i in range(10):
        rcv = port.read(10)
        print "!"+rcv

    return True


def recv_sms():
    port.write('AT'+'\r\n')
    port.write("\x0D\x0A")
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return ('', False)
    sleep(1)
    
    # Disable the Echo
    port.write('ATE0'+'\r\n')                 
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return ('', False)
    sleep(1)
    
    # Select Message format as Text mode
    port.write('AT+CMGF=1'+'\r\n')             
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return ('', False)
    sleep(1)
    
    # New SMS Message Indications
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')      
    rcv = port.read(10)
    print("!"+rcv)
    #if not 'OK' in rcv:
    #    return ('', False)
    sleep(1)

    # TODO move the above to its own method
    
    while True:
        rcv = port.read(10)
        print "!"+rcv
        fd=rcv
        # check if any data received 
        if len(rcv)>3:                   
            for i in range(5):            
                rcv = port.read(10)
                print "!"+rcv
                fd=fd+rcv                
    
            # Extract the message number shown in between the characters "," and '\r'
            p=list(find(fd, ","))
            q=list(find(fd, '\r'))
            MsgNo=fd[p[0]+1:q[1]]         
    
            # Read the message corresponds to the message number
            rd=port.write('AT+CMGR='+MsgNo+'\r\n')
            msg=''
            for j in range(10):
                rcv = port.read(20)
                msg=msg+rcv
            return (msg, True)
        sleep(0.1)

    return ('', False)

def gui_send_sms():
    print("send")
    (number, status) = update_lcd_until_enter(lcd, "Enter number:\n{0}")
    if not status:
        return
    (message, status) = update_lcd_until_enter(lcd, "Enter message:\n{0}", True)
    if not status:
        return
    lcd.clear()
    sleep(1)
    lcd.message("Preparing...")
    status = init_send_sms()
    lcd.clear()
    if not status:
        lcd.message("Failed. :(")
        sleep(2)
        return
    lcd.message("Sending...")
    sleep(1)
    status = send_sms(number, message)
    lcd.clear()
    if not status:
        lcd.message("Failed. :(")
        sleep(2)
        return
    lcd.message("Done.")
    sleep(1)
    return

def gui_recv_sms():
    print("recv")
    (message, status) = recv_sms()
    if not status:
        return
    print(message)
    lcd.message(message)


# --- --- --- --- --- --- --- --- --- --- --- ---

# Main loop
def main():
    while (True):
        lcd.clear()
        lcd.blink(False)
        lcd.message('(1) Send SMS\n(2) Recv SMS')

        ch = rotary() #getch()

        # Check what to do
        if ch == '1':
            gui_send_sms()
        elif ch == '2':
            gui_recv_sms()



if __name__ == "__main__":
    main()
