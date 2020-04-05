import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


# alternate scaled: '?wid=2239&hei=2857&size=2239,2857&qlt=100'


class ASOSGoblin(MetaGoblin):
    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.path_dl = os.path.join(self.path_main, 'fullsize')
        self.path_scanned = os.path.join(self.path_main, 'scanned')
        self.path_backup = os.path.join(self.path_main, 'backup')
        self.path_external = os.path.join(os.getcwd(), 'asos')
        self.query = '?scl=1&qlt=100'

    def __str__(self):
        return 'asos goblin'

    def __repr__(self):
        return 'asos'

    def extract_color(self, url):
        '''
        extract color from url
        '''
        if 'images.asos-media' in url:
            color = re.search(r'\d+\-\d\-\w+', url)
        else:
            color = re.search(r'clr=\w+', url)
        if color:
            return re.sub(r'\d+-\d-', '', color.group().lstrip('clr='))

    def form_url(self, id, large=False):
        '''
        generate a url from an image id
        '''
        id = str(id)
        if not re.search(r'\-[a-z0-9]+$', id):
            id += '-2'
        url = f'https://images.asos-media.com/products/asos/{id}'
        return url + self.query if large else url

    def extract_id(self, url):
        '''
        pull image id from url
        '''
        return re.search(r'\d+', url).group()


    def grab(self, url):
        '''
        grab a single url in high res
        '''
        color = self.extract_color(url)
        id = self.extract_id(url)
        if color:
            self.collect(self.form_url(f'{id}-1-{color}', True))
        for n in range(2, 5):
            self.collect(self.form_url(f'{id}-{n}', True))

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            self.grab(target)
        self.loot()
