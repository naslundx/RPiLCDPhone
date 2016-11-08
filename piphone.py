import RPi.GPIO as GPIO
from pi_hardware import pi_hardware
from pi_modem import pi_modem
from pi_phone import pi_phone
from pi_debug import pi_debug
from time import sleep

print('RPiLCDPhone: Starting.')

GPIO.setmode(GPIO.BCM)

debugger = pi_debug(debug=True)
hardware = pi_hardware(rotary_pin=21, hook_pin=26, ringer_pin=20, debugger=debugger)
modem = pi_modem(hardware=hardware, power_pin=16, debugger=debugger)
phone = pi_phone(hardware=hardware, modem=modem, debugger=debugger)

sleep(0.2)
modem.power_on()
sleep(0.2)
# self.hardware.ring(1.0)

print('RPiLCDPhone: Initialized. Starting loop.')

phone.loop()
