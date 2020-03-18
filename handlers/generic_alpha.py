import re
import os
from handlers.meta_goblin import MetaGoblin

# QUESTION: incomplete?

class AlphaGoblin(MetaGoblin):
    '''
    for media_catalog structures
    '''

    def upgrade(self, path, base):
        '''
        upgrade existing files
        '''
        base = base.rstrip('/')
        for file in os.listdir(path):
            file = re.sub(r'\.(jpe*g|png)', '', file)
            self.retrieve(f'{base}/media/catalog/product/{file[0]}/{file[1]}/{file}.jpg')
            sleep(self.tickrate)

    def run(url):
        self.retrieve(decrop(re.sub(r'cache/\d/\w+/(\d+x\d+/)*\w+/', '', url)))
