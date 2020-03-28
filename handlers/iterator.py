import os
import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class IteratorGoblin(MetaGoblin):

    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'iterator goblin'

    def extract_iterable(self, url):
        '''
        seperate iterable from a url (mode 3)
        '''
        return re.split('%%%', url)

    # IDEA: instead of hard coding 100, maybe use double timeout value.
    # TODO: add reverse?
    def generate_links(self, base, iterable, end):
        stripped_iter = int(iterable.lstrip('0'))
        for n in range(stripped_iter, stripped_iter + 20, self.args['increment']):
            self.collect(f'{base}{str(n).zfill(len(iterable))}{end}')

    def increment_iterable(self, iterable):
        return str(int(iterable.lstrip('0')) + 20).zfill(len(iterable))

    def iterate(self):
        '''
        re-forms url and iterates (mode 3)
        '''
        round = 1
        base, iterable, end = self.extract_iterable(self.args['url'])
        while True:
            print(f'[{self.__str__()}] <iterating> round {round}')
            self.generate_links(base, iterable, end)
            self.toggle_collecton_type()
            attempt = self.loot(timeout=self.args['timeout'])
            if attempt:
                round += 1
                iterable = self.increment_iterable(iterable)
                self.new_collection()
            else:
                print(f'[{self.__str__()}] <timeout> after {self.args["timeout"]} attempts')
                return None

    def run(self):
        self.iterate()
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
