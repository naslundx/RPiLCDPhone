import sys
import tty
import termios
import serial
import RPi.GPIO as GPIO      
import os
from Adafruit_CharLCD import Adafruit_CharLCD
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


# Initialize send SMS
def init_send_sms():
    print("Initializing Send SMS...")
    # Prepare
    port.write('AT\r\n')
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # Disable the Echo
    port.write('ATE0\r\n')      
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # Select Message format as Text mode 
    port.write('AT+CMGF=1\r\n')  
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # New SMS Message Indications
    port.write('AT+CNMI=2,1,0,0,0\r\n')   
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    print("Send SMS Initialized.")
    return True


def send_sms(number, message):
    # Pass on recepient number
    port.write('AT+CMGS="%s"\r\n' % number)
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # Pass on message
    port.write('%s\r\n' % message)
    rcv = port.read(10)
    print rcv
    
    # Send
    port.write("\x1A")
    for i in range(10):
        rcv = port.read(10)
        print rcv

    return True


def recv_sms():
    port.write('AT'+'\r\n')
    port.write("\x0D\x0A")
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # Disable the Echo
    port.write('ATE0'+'\r\n')                 
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # Select Message format as Text mode
    port.write('AT+CMGF=1'+'\r\n')             
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    # New SMS Message Indications
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')      
    rcv = port.read(10)
    if not 'OK' in rcv:
        return False
    sleep(1)
    
    while True:
        rcv = port.read(10)
        print rcv
        fd=rcv
        # check if any data received 
        if len(rcv)>3:                   
            for i in range(5):            
                rcv = port.read(10)
                print rcv
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
            print msg
            return True
        sleep(0.1)


def gui_send_sms():



def gui_recv_sms():


# --- --- --- --- --- --- --- --- --- --- --- ---

# Init serial port
GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

# Init LCD
# TODO

# TODO clear lcd

# Main loop
# def main():
while (True):
    # TODO print "1) Send SMS\n2) Receive SMS"

    ch = getch()
    print(str(ch))

    # Check what to do
    if ch == '1':
        gui_send_sms()
    elif ch == '2':
        gui_recv_sms()



# if __name__ == "__main__":
#     main()