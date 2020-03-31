import re
from handlers.meta_goblin import MetaGoblin


class TheIconicGoblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'(\d+\-){2}\d\.jpg'

    def __str__(self):
        return 'the iconic goblin'

    def extract_id(self, url):
        return re.search(r'\d+\-\d+\-', url).group()

    def run(self):
        if 'img1' in self.args['url'] or 'static' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            id = self.extract_id(link)
            for n in range(1, 6):
                self.collect(f'https://static.theiconic.com.au/p/{id}{n}.jpg')
        self.loot()
