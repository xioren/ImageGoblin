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

    NAME = 'asos goblin'
    ID = 'asos'
    QUERY = '?scl=1&qlt=100'
    URL_BASE = 'https://images.asos-media.com/products/asos/'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        id = re.search(r'\d+(?=-\d)', url) or re.search(r'(?<=/)\d{2,}', url)
        return id.group()

    def extract_color(self, url):
        '''extract color from url'''
        if 'asos.com' in url:
            color = re.search(r'(?<=clr=)[a-z\s]+', url) \
                    or re.search(r'(?<=-1-)[a-z\s]+', self.get(url).content)
        else:
            color = re.search(r'(?<=-1-)[a-z\d]+', url) \
                    or re.search(r'(?<!/\d/\d)/[a-z\s]+(?=/[^/]+$)', url)
        return color.group().lstrip('/') if color else ''

    def form_url(self, id):
        '''generate a url from an image id'''
        return f'{self.URL_BASE}{id}{self.QUERY}'

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            color = self.extract_color(target)
            id = self.extract_id(target)
            if color:
                self.collect(self.form_url(f'{id}-1-{color}'))
            for n in range(2, 5):
                self.collect(self.form_url(f'{id}-{n}'))
        self.loot()
