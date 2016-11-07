import RPi.GPIO as GPIO
from pi_hardware import pi_hardware
from pi_modem import pi_modem
from pi_phone import pi_phone
from time import sleep

GPIO.setmode(GPIO.BCM)

hardware = pi_hardware(rotary_pin=21, hook_pin=26, ringer_pin=20, debug=True)
modem = pi_modem(hardware=hardware, power_pin=16, debug=True)
phone = pi_phone(hardware=hardware, modem=modem, debug=True)

sleep(1.0)
modem.power_on()
sleep(1.0)
# self.hardware.ring(1.0)
phone.loop()
