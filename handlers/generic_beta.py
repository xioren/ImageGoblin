import re
from handlers.meta_goblin import MetaGoblin


class BetaGoblin(MetaGoblin):

    '''
    handles: Adobe Dynamic Media Image Serving and Image Rendering API (scene7)
    docs: https://docs.adobe.com/content/help/en/dynamic-media-developer-resources/image-serving-api/image-serving-api/http-protocol-reference/command-reference/c-command-reference.html
    accepts:
        - image
        - webpage
    generic backend for:
        - anthropologie
        - calvin klein
        - esprit
        - free people
        - hot topic
        - tommy hilfiger
        - urban outfitters
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pat = r'\w+\.scene7[^" \n]+'
        self.query = '?fmt=jpeg&qlt=100&scl=1'

    def extract_id(self, url):
        return re.search(r'[A-Za-z0-9]+_([A-Za-z0-9]+)*', url).group()

    def correct_format(self, url):
        if re.search(r'[a-z0-9]+_([a-z0-9]+)*', url):
            return True
        else:
            return False

    def run(self):
        if 'scene7' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pat, self.args['url'])
        for link in links:
            if not self.correct_format(link):
                continue
            base = self.identify(link)
            id = self.extract_id(link)
            for mod in self.modifiers:
                self.collect(f'{base}{id}_{mod}{self.query}')
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
