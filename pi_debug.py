from time import gmtime, strftime

class pi_debug:
    def __init__(self, debug=False):
        self.debug = debug

    def out(message):
        now = strftime("%H:%M:%S", gmtime())
        print(now + ': ' + message)
