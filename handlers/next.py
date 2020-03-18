import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


class NextGoblin(MetaGoblin):

    '''
    mode options:
        - +: iterate forward
        - -: iterate backward
    link types:
        - image
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.base = 'https://s3.amazonaws.com/next-management-production/assets/images/'
        self.alt = 'https://res.cloudinary.com/next-management/image/upload/photos/'
        self.filtypes = ('JPG', 'jpg', 'PNG', 'png', 'JPEG', 'jpeg')
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'next goblin'

    def extract(self, link):
        return int(re.search(r'\d{4,10}', link).group())

    def upgrade(self, path):
        # QUESTION: does this work?
        for file in os.listdir(path):
            self.loot(f'{base}{file[:-4]}/original{file[-4:]}', filename=file[:-4])
            sleep(self.tickrate)

    def run(self):
        id = self.extract(self.url)
        while True:
            for type in self.filtypes:
                attempt = self.loot(f'{base}{id}/medium_portrait.{type}', filename=id)
                if attempt:
                    break
                sleep(self.tickrate)
            if self.mode == '-':
                id -= 1
            else:
                id += 1
            sleep(self.tickrate)
