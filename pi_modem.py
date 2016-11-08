from pi_hardware import pi_hardware
from time import sleep


class pi_modem:
    def __init__(self, hardware, power_pin, debugger):
        self.debugger = debugger
        self.hardware = hardware
        self.power_pin = power_pin
        self.hardware.set_pin_out(self.power_pin)

    def power_on(self):
        self.hardware.pin_on(self.power_pin, 2.0)

    def caller_id(self):
        self.hardware.serial_write('AT+CLIP=1')
        rcv = self.hardware.serial_read()

    def check_status(self):
        sleep(0.1)
        self.hardware.serial_write('AT')
        rcv = self.hardware.serial_read()
        status = 'OK' in rcv
        self.debugger.out('Modem status=' + str(status))
        return status

    def call(self, number):
        if not self.check_status():
            return

        self.hardware.serial_write('ATD' + number + ';')
        rcv = self.hardware.serial_read()

    def hang_up(self):
        self.hardware.serial_write('ATH')
        rcv = self.hardware.serial_read()

    def check_incoming_call(self):
        if not self.check_status():
            return

        rcv = self.hardware.serial_read()

        if 'RING' in rcv:
            number = rcv.split(',')[0].split(': ')[1].replace('"', '')
            self.debugger.out("Incoming number='" + number + "'")
            return number

        return None

    def receive(self):
        self.hardware.serial_write('ATA')
        rcv = self.hardware.serial_read()
