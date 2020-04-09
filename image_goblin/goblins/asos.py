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

    def __str__(self):
        return 'asos goblin'

    def __repr__(self):
        return 'asos'

    def extract_color(self, url):
        '''extract color from url'''
        if 'images.asos-media' in url:
            color = re.search(r'\d+\-1\-[a-z0-9]+', url).group()
        else:
            try:
                color = re.search(r'clr=\w+', url).group().lstrip('clr=')
            except AttributeError:
                # QUESTION: add hiphen to re?
                color = self.extract_urls(r'\d+-1-[a-z0-9]+', url).pop()
        return re.sub(r'\d+-\d-', '', color)

    def form_url(self, id, large=False):
        '''generate a url from an image id'''
        id = str(id)
        if not re.search(r'\-[a-z0-9]+$', id):
            id += '-2'
        url = f'https://images.asos-media.com/products/asos/{id}'
        return url + '?scl=1&qlt=100' if large else url

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            color = self.extract_color(target)
            id = re.search(r'\d{5,}', target).group()
            if color:
                self.collect(self.form_url(f'{id}-1-{color}', True))
            for n in range(2, 5):
                self.collect(self.form_url(f'{id}-{n}', True))
        self.loot()
