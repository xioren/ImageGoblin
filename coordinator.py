import re
import os
from manifest import handlers


class Coordinator:

    def __init__(self, args):
        self.args = args

    def identify(self, url):
        for key in handlers:
            if re.search(handlers[key][0], url, re.IGNORECASE):
                return key
        return 'generic'

    def deploy(self):
        url_assignment = {}
        if self.args['list']:
            for key in handlers:
                print(key)
            return
        elif self.args['local']:
            with open(os.path.join(os.getcwd(), self.args['local'])) as file:
                urls = set(file.read().splitlines())
        elif self.args['feed']:
            goblin = handlers['hungry'][1]
            urls = goblin().run()
        else:
            urls = [self.args['targets']]
        for url in urls:
            handler = self.identify(url)
            if url_assignment.get(handler):
                url_assignment[handler].append(url)
            else:
                url_assignment[handler] = [url]
        self.args['targets'] = url_assignment
        if self.args['force']:
            goblin = handlers[self.args['force']][1]
            goblin(self.args).run()
        else:
            for handler in url_assignment:
                goblin = handlers[handler][1]
                goblin(self.args).run()
