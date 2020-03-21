import re
import os
from manifest import handlers


class Coordinator:

    def __init__(self, args):
        self.args = args

    def identify(self, link):
        for key in handlers:
            if re.search(handlers[key][0], link, re.IGNORECASE):
                return handlers[key][1]
        return handlers['generic'][1]

    def deploy(self):
        if self.args['list']:
            for key in handlers:
                print(key)
            return
        elif self.args['local']:
            with open(os.path.join(os.getcwd(), self.args['local'])) as file:
                links = set(file.read().splitlines())
        else:
            links = [self.args['url']]
        for link in links:
            self.args['url'] = link
            if self.args['handler']:
                goblin = self.identify(self.args['handler'])
            else:
                goblin = self.identify(self.args['url'])
            goblin(self.args).run()
