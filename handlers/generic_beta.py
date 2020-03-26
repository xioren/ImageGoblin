import re
from handlers.meta_goblin import MetaGoblin


class BetaGoblin(MetaGoblin):

    '''
    for scen7 variants
    accepts:
        - image
        - webpage
    generic backend for:
        - anthropologie
        - calvin klein
        - free people
        - hot topic
        - tommy hilfiger
        - urban outfitters
    '''

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        return re.search(r'[a-z0-9]+_([a-z0-9]+)*', url).group()

    def correct_format(self, url):
        if re.search(r'[a-z0-9]+_([a-z0-9]+)*', url):
            return True
        else:
            return False

    def run(self):
        if 'scene7' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'\w+\.scene7[^" \n]+', self.args['url'])
        for link in links:
            if not self.correct_format(link):
                continue
            base, query = self.identify(link)
            id = self.extract_id(link)
            for char in self.chars:
                self.collect(f'{base}{id}_{char}{query}')
        self.loot()
