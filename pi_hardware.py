import sys
import tty
import termios
import serial
from time import sleep
import RPi.GPIO as GPIO


class pi_hardware:
    def __init__(self, rotary_pin, hook_pin, ringer_pin, debugger):
        self.debugger = debugger
        self.rotary_pin = rotary_pin
        self.set_pin_in(self.rotary_pin)
        self.hook_pin = hook_pin
        self.set_pin_in(self.hook_pin)
        self.ringer_pin = ringer_pin
        self.set_pin_out(self.ringer_pin)
        ttyama0 = '/dev/ttyAMA0'
        self.serial_port = serial.Serial(ttyama0, baudrate=9600, timeout=1)

    def set_pin_in(self, pin):
        self.debugger.out("#%d set to IN" % pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_pin_out(self, pin):
        self.debugger.out("#%d set to OUT" % pin)
        GPIO.setup(pin, GPIO.OUT)
        self.pin_off(pin)

    def read_pin(self, pin, write_to_debug=True):
        result = (GPIO.input(pin) != 0)
        if write_to_debug:
            self.debugger.out("#%d reads %s" % (pin, result))
        return result

    def pin_on(self, pin, time):
        self.debugger.out("Voltage on #%d" % pin)
        GPIO.output(pin, GPIO.HIGH)
        self.debugger.wait(time)
        self.pin_off(pin)

    def pin_off(self, pin):
        self.debugger.out("Voltage off #%d" % pin)
        GPIO.output(pin, GPIO.LOW)

    def ring(self, time):
        self.pin_on(self.ringer_pin, time)

    def hook_lifted(self):
        return self.read_pin(self.hook_pin, write_to_debug=False)

    def serial_flush(self):
        bus = self.serial_read()
        self.debugger.out("Flushed '%s'" % bus)

    def serial_write(self, message):
        self.debugger.out("Serial out: '%s'" % message)
        self.serial_port.write(message + '\r\n')

    def serial_read(self):
        full_message = ""
        iterations = 5
        while iterations > 0:
            iterations -= 1
            self.debugger.wait(0.05)
            message = self.serial_port.read(25)
            if message:
                full_message = full_message + message
            else:
                break

        full_message = full_message.replace('\r\n', ' ').replace('\n', ' ')
        self.debugger.out("Serial in: '%s'" % full_message)
        return full_message

    def get_rotary(self):
        no_digit_counter = 0
        number = ''
        while self.hook_lifted() and no_digit_counter < 20:
            self.debugger.wait(0.05)
            next_digit = self.get_rotary_digit()
            if next_digit:
                number = number + next_digit
                self.debugger.out('Number=%s' % number)
                no_digit_counter = 0
            else:
                no_digit_counter += 1
        return number

    def get_rotary_digit(self):
        flag = False
        counter = 0
        false_flag_tick = 0
        while self.hook_lifted():
            sleep(0.001)
            new_flag = (self.read_pin(self.rotary_pin, write_to_debug=False))
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
                    return result
                else:
                    break
        return None
