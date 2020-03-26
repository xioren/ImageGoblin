import re
from handlers.meta_goblin import MetaGoblin


class MangoGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'mango goblin'

    def extract_id(self, url):
        return re.search(r'T\d', url).group(), re.search(r'\d+_\d+', url).group()

    def run(self):
        if 'mngbcn' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'https://st\.mngbcn\.com[^"\? ]+\.jpg', self.args['url'])
        for link in links:
            t, id = self.extract_id(link)
            self.collect(f'https://st.mngbcn.com/rcs/pics/static/{t}/fotos/outfit/S20/{id}-99999999_01.jpg')
            for mod in ('', '_R', '_D1', '_D2', '_D3', '_D4', '_D5', '_D6'):
                self.collect(f'https://st.mngbcn.com/rcs/pics/static/{t}/fotos/S20/{id}{mod}.jpg')
        self.loot()
