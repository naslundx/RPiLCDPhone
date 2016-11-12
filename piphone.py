import RPi.GPIO as GPIO
from pi_hardware import pi_hardware
from pi_modem import pi_modem
from pi_phone import pi_phone
from pi_debug import pi_debug
from time import sleep

GPIO.setmode(GPIO.BCM)

debugger = pi_debug(debug=True)
hardware = pi_hardware(rotary_pin=21, hook_pin=26, ringer_pin=20, debugger=debugger)
modem = pi_modem(hardware=hardware, power_pin=18, debugger=debugger)
phone = pi_phone(hardware=hardware, modem=modem, debugger=debugger)

# hardware.ring(1.0)

sleep(0.5)
debugger.out('RPiLCDPhone: Initialized. Starting loop.')

phone.loop(force_start=False)
