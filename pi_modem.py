from pi_hardware import pi_hardware


class pi_modem:
    def __init__(self, hardware, power_pin, allow_restart, debugger):
        self.debugger = debugger
        self.hardware = hardware
        self.power_pin = power_pin
        self.allow_restart = allow_restart
        self.hardware.set_pin_out(self.power_pin)
        self.empty_response_count = 0

    def power_on(self):
        self.empty_response_count = 0
        self.hardware.pin_on(self.power_pin, 2.0)

    def caller_id(self):
        self.hardware.serial_write('AT+CLIP=1')
        rcv = self.hardware.serial_read()

    def check_status(self):
        self.debugger.wait(0.1)
        self.hardware.serial_write('AT')
        rcv = self.hardware.serial_read()
        status = 'OK' in rcv
        self.debugger.out('Modem status=%s' % str(status))
        if len(rcv.strip()) == 0:
            self.empty_response_count += 1
            self.debugger.out('Modem appears turned off? (%d)' % self.empty_response_count)
        return status

    def no_modem_response(self):
        return (self.empty_response_count > 3)

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
