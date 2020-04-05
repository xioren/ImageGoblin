import re
import os
from manifest import goblins


class Dispatcher:

    def __init__(self, args):
        self.args = args

    def identify(self, url):
        for key in goblins:
            if re.search(goblins[key][0], url, re.IGNORECASE):
                return key
        return 'generic'

    def dispatch(self):
        url_assignment = {}
        if self.args['list']:
            for key in goblins:
                print(key)
            return
        elif self.args['local']:
            with open(os.path.join(os.getcwd(), self.args['local'])) as file:
                urls = set(file.read().splitlines())
        elif self.args['feed']:
            goblin = goblins['hungry'][1]
            urls = goblin().run()
        else:
            urls = [self.args['targets']]
        for url in urls:
            key = self.identify(url)
            if url_assignment.get(key):
                url_assignment[key].append(url)
            else:
                url_assignment[key] = [url]
        self.args['targets'] = url_assignment
        if self.args['force']:
            goblin = goblins[self.args['force']][1]
            goblin(self.args).run()
        else:
            for key in url_assignment:
                goblin = goblins[key][1]
                goblin(self.args).run()
