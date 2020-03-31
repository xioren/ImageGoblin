import re
from handlers.meta_goblin import MetaGoblin


class SavageXGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'https*://[^" \n]+\d\-800x800.jpg'

    def __str__(self):
        return 'savagex goblin'

    def strip(self, url):
        return re.sub(r'(LAYDOWN|\d)\-\d+x\d+.jpg', '', url)

    def run(self):
        if 'cdn.savagex' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            for n in range(1, 5):
                self.collect(self.strip(link) + f'{n}-1600x1600.jpg')
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
