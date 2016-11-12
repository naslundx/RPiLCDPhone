from time import gmtime, strftime, sleep


class pi_debug:
    def __init__(self, debug=False):
        self.debug = debug

    def out(self, message):
        now = strftime("%H:%M:%S", gmtime())
        print(now + ': ' + message)

    def wait(self, time):
        self.out('(Sleeping for %f s)' % time)
        sleep(time)
