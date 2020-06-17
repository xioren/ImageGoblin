from goblins.meta import MetaGoblin

# TODO:
#   - implement natural sorting?
#   - add webpage handling
#   - handle urls containing #

class IteratorGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    NAME = 'iterator goblin'
    ID = 'iterator'

    def __init__(self, args):
        super().__init__(args)
        self.block_size = self.args['step'] * 100

    def unique(self, url, other_url):
        '''check if filenames are unique'''
        if self.parser.extract_filename(url) == self.parser.extract_filename(other_url):
            return False
        return True

    def isolate_parts(self, url):
        '''seperate url into base, iterable, end'''
        return url.split('#')

    def strip_iterable(self, full_iterable):
        '''strip leading zeros'''
        if all(n == '0' for n in full_iterable):
            return 0
        return int(full_iterable.lstrip('0'))

    def increment_iterable(self, iterable):
        '''increment the iterable by blocksize'''
        return str(self.strip_iterable(iterable) + self.block_size).zfill(len(iterable))

    def generate_block(self, base, iterable, end):
        '''generate block of urls to iterate over'''
        stripped_iter = self.strip_iterable(iterable)

        for n in range(stripped_iter, stripped_iter + self.block_size, self.args['step']):
            if self.is_unique:
                filename = ''
            else:
                filename = str(n)

            self.collect(f'{base}{str(n).zfill(len(iterable))}{end}', filename=filename)

    def run(self):
        '''main iteration method'''
        round = 1
        self.toggle_collecton_type() # convert collection to list so that urls are ordered
        base, iterable, end = self.isolate_parts(self.args['targets'][self.ID][0])
        self.is_unique = self.unique(f'{base}{iterable}{end}', f'{base}{self.increment_iterable(iterable)}{end}')

        while True:
            self.logger.log(1, self.NAME, 'iterating', f'round: {round} || block: {iterable}-{self.strip_iterable(iterable)+self.block_size-self.args["step"]}')
            self.generate_block(base, iterable, end)

            timedout = self.loot(timeout=self.args['timeout'])
            if timedout:
                self.logger.log(1, self.NAME, 'timed out', f'after {self.args["timeout"]} attempts')
                return None
            else:
                round += 1
                iterable = self.increment_iterable(iterable)
                self.new_collection()
