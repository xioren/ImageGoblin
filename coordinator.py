import re
from manifest import handlers


class Coordinator:

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        self.url = url
        self.mode = mode
        self.timeout = timeout
        self.format = format
        self.increment = increment
        self.nodl = nodl
        self.verbose = verbose
        self.tickrate = tickrate

    def identify(self):
        for key in handlers:
            if re.search(handlers[key][0], self.url):
                return handlers[key][1]
        return handlers['generic_omega'][1]

    def deploy(self):
        goblin = self.identify()
        goblin(self.url, self.mode, self.timeout,
               self.format, self.increment, self.nodl,
               self.verbose, self.tickrate).run()
