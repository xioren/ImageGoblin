from time import sleep
from goblin import MetaGoblin
from parsing import *


class IterGoblin(MetaGoblin):

    def __init__(self, url, timeout, save_loc, overwrite, increment):
        super().__init__(url=url, save_loc=save_loc, overwrite=overwrite)
        self.timeout = timeout
        self.idle = 0
        self.increment = increment

    def timeout_check(self, n):
        '''
        program idle tracking
        '''
        if n > 0 and self.idle >= n:
            return True
        else:
            return False

    def iter_mod(self, iter):
        '''
        increment the iterable containing arbitray leading zeros
        '''
        return str(int(iter.lstrip('0')) + self.increment).zfill(len(iter))

    def iterate(self):
        '''
        re-forms url and iterates (mode 3)
        '''
        base, iter, end = iter_finder(url=self.url)
        self.create_folders(self.dl_folder)
        iteration = 1
        print(f'[iterating] {self.url}')
        while True:
            if self.timeout_check(self.timeout):
                self.cleanup(self.dl_folder)
                print(f'[timeout] after {self.timeout} attempts')
                return
            if iteration % 25 == 0:
                print(f'[iteration] {iteration}')
            url, filename = dl_prep(url=f'{base}{iter}{end}')
            if not self.overwrite and self.exists(f'{self.dl_folder}{filename}'):
                continue
            success = self.retrieve(url=url, path=f'{self.dl_folder}{filename}', silent=True)
            if success:
                self.idle = 0
            else:
                self.idle += 1
            iter = self.iter_mod(iter)
            iteration += 1
            sleep(1)
