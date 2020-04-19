import re
import os

from manifest import goblins


class Dispatcher:

    def __init__(self, args):
        self.args = args

    def __str__(self):
        return 'dispatcher'

    def identify(self, url):
        '''match url to a specific goblin'''
        for key in goblins:
            if re.search(f'(?:{goblins[key][0]})', url, re.IGNORECASE):
                return key
        return 'generic'

    def dispatch(self):
        '''identify and deploy goblins'''
        url_assignment = {}
        if self.args['list']:
            for key in goblins:
                print(key)
            return None
        elif self.args['local']:
            with open(os.path.join(os.getcwd(), self.args['local'])) as file:
                urls = set(file.read().splitlines())
        elif self.args['feed']:
            goblin = goblins['hungry'][1]
            urls = goblin().run()
        else:
            if not self.args['targets']:
                print(f'[{self.__str__()}] <ERROR> input not understood')
                return None
            urls = [self.args['targets']]
        for url in urls:
            if self.args['force']:
                key = self.args['force']
            elif self.args['greedy']:
                key = 'generic'
            else:
                key = self.identify(url)
            if url_assignment.get(key):
                url_assignment[key].append(url)
            else:
                url_assignment[key] = [url]
        self.args['targets'] = url_assignment
        for key in url_assignment:
            try:
                goblin = goblins[key][1]
            except KeyError:
                print(f'[{self.__str__()}] <ERROR> unkown goblin -> use --list to see available goblins')
                return None
            goblin(self.args).run()
