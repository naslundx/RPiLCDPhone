from time import sleep
import sys
import tty
import termios
import serial
import RPi.GPIO as GPIO

class pi_hardware:
    def __init__(self, rotary_pin, hook_pin, ringer_pin, debug=False):
	self.debug = debug
        self.rotary_pin = rotary_pin
        self.set_pin_in(self.rotary_pin)
        self.hook_pin = hook_pin
        self.set_pin_in(self.hook_pin)
        self.ringer_pin = ringer_pin
        self.set_pin_out(self.ringer_pin)
        self.serial_port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)


    def set_pin_in(self, pin):
        if self.debug:
            print("Pin #" + str(pin) + " set to IN")
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def set_pin_out(self, pin):
        if self.debug:
            print("Pin #" + str(pin) + " set to OUT and LOW")
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)


    def read_pin(self, pin):
        result = (GPIO.input(pin) != 0)
        if self.debug:
            print("Pin #" + str(pin) + " reads " + str(result))
        return result


    def pin_on(self, pin, time):
        if self.debug:
            print("Voltage on pin #" + str(pin) + " for " + str(time) + "s")
        GPIO.output(pin, GPIO.HIGH)
        sleep(time)
        GPIO.output(pin, GPIO.LOW)


    def ring(self, time):
        self.pin_on(self.ringer_pin, time)


    def hook_lifted(self):
        return self.read_pin(self.hook_pin)

    
    def serial_write(self, message):
        if self.debug:
            print("Serial out:\t" + message)
        self.serial_port.write(message + '\r\n')


    def serial_read(self):
        full_message = ""
        iterations = 5
        while iterations > 0:
            iterations -= 1
            sleep(0.1)
            message = self.serial_port.read(10)
            if message:
                full_message = full_message + message
            else:
                break
        
        full_message = full_message.replace('\r\n',' ').replace('\n',' ')
        if self.debug:
            print("Serial in:\t" + full_message)
        return full_message


    def get_rotary(self):
        # flag = False
        # counter = 0
        # false_flag_tick = 0
        # while self.hook_lifted():
        #     sleep(0.001)
        #     new_flag = (self.read_pin(self.rotary_pin))
        #     if flag != new_flag:
        #         counter += 1
        #         flag = new_flag
        #     if not flag:
        #         false_flag_tick += 1
        #     else:
        #         false_flag_tick = 0

        #     if false_flag_tick > 100:
        #         ctr = int(counter / 2) - 1
        #         if ctr >= 0:
        #             result = str(ctr)
        #             print(result)
        #             return result
        #         else:
        #             break
            
        # return None

        sleep(1.0)
        return '0738299658'
