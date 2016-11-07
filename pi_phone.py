from pi_hardware import pi_hardware
from pi_modem import pi_modem
from time import sleep

class pi_phone:
    def __init__(self, hardware, modem, debug=False):
        self.hardware = hardware
        self.modem = modem
        self.modem.caller_id()
        self.debug = debug


    def loop(self):
        sleep(0.5)
        self.hardware.ring(1.0)
        sleep(0.5)
        while True:
            if self.debug:
                print('.')
            sleep(0.5)
            if self.hardware.hook_lifted():
                self.make_call()
            else:
                self.receive_call()

    
    def make_call(self):
        number = self.hardware.get_rotary()
        if not self.hardware.hook_lifted():
            return

        self.modem.call(number)
        while self.hardware.hook_lifted():
            sleep(1.0)

        self.modem.hang_up()

    
    def receive_call(self):
        incoming = self.modem.check_incoming_call()
        if incoming:
            while not self.hardware.hook_lifted():
                self.hardware.ring(0.5)
                sleep(0.5)
                incoming = self.modem.check_incoming_call()
                
            self.modem.receive()

            while self.hardware.hook_lifted():
                sleep(0.5)

            self.modem.hang_up()
