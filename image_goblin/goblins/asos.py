import re
import os

from time import sleep
from goblins.meta import MetaGoblin


# alternate scaled query: '?wid=2239&hei=2857&size=2239,2857&qlt=100'
# alternate url format: https://images.asos-media.com/inv/media/7/6/5/4/01234567/color/image1xxl.jpg

class ASOSGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.query = '?scl=1&qlt=100'
        self.url_base = 'https://images.asos-media.com/products/asos/'

    def __str__(self):
        return 'asos goblin'

    def __repr__(self):
        return 'asos'

    def extract_id(self, url):
        '''extract image id from url'''
        id = re.search(r'\d+(?=-[0-9])', url) or re.search(r'(?<=/)\d{2,}', url)
        return id.group()

    def extract_color(self, url):
        '''extract color from url'''
        if 'asos.com' in url:
            color = re.search(r'(?<=clr=)[a-z0-9]+', url) or re.search(r'(?<=-1-)[a-z0-9]+', self.get_response(url))
        else:
            color = re.search(r'(?<=-1-)[a-z0-9]+', url) or re.search(r'(?<!/\d/\d)/[a-z0-9]+(?=/[^/]+$)', url)
        return color.group().lstrip('/') if color else ''

    def form_url(self, id):
        '''generate a url from an image id'''
        return f'{self.url_base}{id}{self.query}'

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            color = self.extract_color(target)
            id = self.extract_id(target)
            if color:
                self.collect(self.form_url(f'{id}-1-{color}'))
            for n in range(2, 5):
                self.collect(self.form_url(f'{id}-{n}'))
        self.loot()
