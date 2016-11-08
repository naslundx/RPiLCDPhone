from pi_hardware import pi_hardware
from pi_modem import pi_modem
from time import sleep


class pi_phone:
    def __init__(self, hardware, modem, debugger):
        self.debugger = debugger
        self.hardware = hardware
        self.modem = modem

    def loop(self, force_start=False):
        self.debugger.out("Initializing modem...")
        while True:
            sleep(0.5)
            self.modem.power_on()
            sleep(0.5)
            if self.modem.check_status():
                break
            elif force_start:
                self.debugger.out("Failed, but forcing start.")
                break
            else:
                self.debugger.out("Failed, making new attempt.")

        self.modem.caller_id()

        while True:
            sleep(1.0)
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
        while incoming and not self.hardware.hook_lifted():
            self.hardware.ring(1.0)
            sleep(0.05)
            incoming = self.modem.check_incoming_call()

        if incoming:
            self.debugger.out('Receiving call')
            self.modem.receive()
            while self.hardware.hook_lifted():
                sleep(0.5)

            self.modem.hang_up()
