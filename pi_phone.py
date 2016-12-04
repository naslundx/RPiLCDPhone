from pi_hardware import pi_hardware
from pi_modem import pi_modem


class pi_phone:
    def __init__(self, hardware, modem, debugger):
        self.debugger = debugger
        self.hardware = hardware
        self.modem = modem

    def loop(self):
        self.hardware.serial_flush()
        if not self.modem.check_status():
            self.power_on_modem()
        self.modem.caller_id()

        if self.hardware.hook_lifted():
            self.debugger.out('Waiting on hook.')
            while self.hardware.hook_lifted():
                self.debugger.wait(0.4)

        self.hardware.ring(0.5)

        while True:
            print('')
            self.debugger.wait(0.1)
            if self.modem.no_modem_response() and self.modem.allow_restart:
                self.power_on_modem()

            if self.hardware.hook_lifted():
                self.make_call()
            else:
                self.receive_call()

    def power_on_modem(self):
        self.debugger.out("Initializing modem...")
        while True:
            self.debugger.wait(1.0)
            self.modem.power_on()
            self.debugger.wait(5.0)
            if self.modem.check_status():
                break
            elif not self.modem.allow_restart:
                self.debugger.out("Failed, but forcing start.")
                break
            else:
                self.debugger.out("Failed, making new attempt.")

    def make_call(self):
        number = self.hardware.get_rotary()
        if len(number) < 3 or not self.hardware.hook_lifted():
            self.debugger.out("No number or hook returned!")
            return

        if not self.modem.check_status():
            self.debugger.out("Failed to make call, modem off!")
            return

        self.modem.call(number)
        while self.hardware.hook_lifted():
            self.debugger.wait(0.5)
        self.modem.hang_up()

    def receive_call(self):
        incoming = self.modem.check_incoming_call()
        while incoming and not self.hardware.hook_lifted():
            self.hardware.ring(1.0)
            self.debugger.wait(0.05)
            incoming = self.modem.check_incoming_call()

        if incoming:
            self.debugger.out('Receiving call')
            self.modem.receive()
            while self.hardware.hook_lifted():
                self.debugger.wait(0.5)

            self.modem.hang_up()
