import re

from goblins.meta import MetaGoblin

# TODO: implement natural sorting

class IteratorGoblin(MetaGoblin):
    '''accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'iterator goblin'

    def __repr__(self):
        return 'iterator'

    def extract_iterable(self, url):
        '''seperate iterable from a url (mode 3)'''
        return re.split('@@@', url)

    # IDEA: instead of hard coding 50, maybe use dynamic value.
    # possibly based on timeout value.
    # TODO: add reverse.
    def generate_urls(self, base, iterable, end):
        '''generate block of urls to iterate over'''
        stripped_iter = int(iterable.lstrip('0'))
        for n in range(stripped_iter, stripped_iter + 50, self.args['increment']):
            self.collect(f'{base}{str(n).zfill(len(iterable))}{end}')

    def increment_iterable(self, iterable):
        return str(int(iterable.lstrip('0')) + 50).zfill(len(iterable))

    def iterate(self):
        '''main iteration method'''
        self.toggle_collecton_type()
        round = 1
        base, iterable, end = self.extract_iterable(self.args['targets'][self.__repr__()][0])
        while True:
            print(f'[{self.__str__()}] <iterating> round {round}')
            self.generate_urls(base, iterable, end)
            _, timeout = self.loot(timeout=self.args['timeout'])
            if not timeout:
                round += 1
                iterable = self.increment_iterable(iterable)
                self.new_collection()
            else:
                print(f'[{self.__str__()}] <timeout> after {self.args["timeout"]} attempts')
                return None

    def run(self):
        self.iterate()
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')