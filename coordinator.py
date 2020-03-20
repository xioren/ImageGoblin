import re
import os
from manifest import handlers


class Coordinator:

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate, local, handler):
        self.url = url
        self.mode = mode
        self.timeout = timeout
        self.format = format
        self.increment = increment
        self.nodl = nodl
        self.verbose = verbose
        self.tickrate = tickrate
        self.local= local
        self.handler = handler

    def identify(self, link):
        for key in handlers:
            if re.search(handlers[key][0], link, re.IGNORECASE):
                return handlers[key][1]
        return handlers['generic'][1]

    def deploy(self):
        if self.local:
            with open(os.path.join(os.getcwd(), self.url)) as file:
                links = set(file.read().splitlines())
        else:
            links = [self.url]
        for link in links:
            if self.handler:
                goblin = self.identify(self.handler)
            else:
                goblin = self.identify(link)
            goblin(link, self.mode, self.timeout,
                   self.format, self.increment, self.nodl,
                   self.verbose, self.tickrate).run()
