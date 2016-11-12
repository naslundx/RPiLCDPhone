from time import gmtime, strftime, sleep


class pi_debug:
    def __init__(self, debug=False):
        self.debug = debug

    def out(self, message):
        now = strftime("%H:%M:%S", gmtime())
        print(now + ': ' + message)

    def wait(self, time):
        if time > 0.2:
            self.out('(Sleeping for %.1f s)' % time)
        sleep(time)
