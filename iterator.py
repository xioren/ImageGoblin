import os
from time import sleep
from goblin import MetaGoblin
from parsing import *


class IterGoblin(MetaGoblin):

    def __init__(self, url, timeout, increment, tickrate, verbose, nodl):
        super().__init__(url, tickrate, verbose, nodl)
        self.timeout = timeout
        self.idle = 0
        self.increment = increment

    def timed_out(self, n):
        '''
        program idle tracking
        '''
        if n > 0 and self.idle >= n:
            return True
        else:
            return False

    def iterate(self):
        '''
        re-forms url and iterates (mode 3)
        '''
        base, iter, end = extract_iterable(self.url)
        iteration = 1
        print(f'[iterating] {self.url}')
        while True:
            url = f'{base}{iter}{end}'
            if self.timed_out(self.timeout):
                self.cleanup(self.main_path)
                print(f'[timeout] after {self.timeout} attempts')
                return None
            if iteration % 25 == 0:
                print(f'[iteration] # {iteration}')
            filename = extract_filename(url)
            filepath = os.path.join(self.main_path, f'{filename}.{filetype(self.url)}')
            if os.path.exists(filepath):
                print(f'[file exists] {filename}')
                continue
            attempt = self.retrieve(url, filepath)
            if attempt:
                self.idle = 0
            else:
                self.idle += 1
            iter = str(int(iter.lstrip('0')) + self.increment).zfill(len(iter))
            iteration += 1
            sleep(self.tickrate)
