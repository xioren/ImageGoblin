import re

from goblins.meta import MetaGoblin

# TODO:
#   - implement natural sorting
#   - add webpage handling

class IteratorGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    NAME = 'iterator goblin'
    ID = 'iterator'

    def __init__(self, args):
        super().__init__(args)
        self.block_size = self.args['step'] * 100

    def isolate_parts(self, url):
        '''seperate url into base, iterable, end'''
        return re.split('#', url)

    def isolate_iterable(self, url):
        '''isolate iterable from url'''
        return int(url.lstrip('0'))

    def generate_urls(self, base, iterable, end):
        '''generate block of urls to iterate over'''
        stripped_iter = self.isolate_iterable(iterable)
        for n in range(stripped_iter, stripped_iter + self.block_size, self.args['step']):
            self.collect(f'{base}{str(n).zfill(len(iterable))}{end}')

    def increment_iterable(self, iterable):
        '''increment the iterable by blocksize'''
        return str(self.isolate_iterable(iterable) + self.block_size).zfill(len(iterable))

    def iterate(self):
        '''main iteration method'''
        self.toggle_collecton_type()
        round = 1
        base, iterable, end = self.isolate_parts(self.args['targets'][self.ID][0])
        while True:
            self.logger.log(1, self.NAME, 'iterating', f'round {round}')
            self.generate_urls(base, iterable, end)
            timeout = self.loot(timeout=self.args['timeout'])
            if timeout:
                self.logger.log(1, self.NAME, 'timeout', f'after {self.args["timeout"]} attempts')
                return None
            else:
                round += 1
                iterable = self.increment_iterable(iterable)
                self.new_collection()

    def run(self):
        self.iterate()
