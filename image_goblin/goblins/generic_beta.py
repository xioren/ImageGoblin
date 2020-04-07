import re

from goblins.meta import MetaGoblin


# NOTE: fmt=png works as well


class BetaGoblin(MetaGoblin):
    '''handles: Adobe Dynamic Media Image Serving and Image Rendering API (scene7)
    docs: https://docs.adobe.com/content/help/en/dynamic-media-developer-resources/image-serving-api/image-serving-api/http-protocol-reference/command-reference/c-command-reference.html
    accepts:
        - image
        - webpage
    generic backend for:
        - american apparel
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
        self.url_pat = r'\w+\.scene7[^" \n]+'
        self.query = '?fmt=jpeg&qlt=100&scl=1'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'[A-Za-z0-9]+_([A-Za-z0-9]+)*', url).group()

    def correct_format(self, url):
        '''check if the url is of the correct format'''
        if re.search(r'[a-z0-9]+_([a-z0-9]+)*', url):
            return True
        else:
            return False

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            if 'scene7' in target:
                urls = [target]
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                if not self.correct_format(url):
                    continue
                url_base = self.identify(url)
                id = self.extract_id(url)
                for mod in self.modifiers:
                    self.collect(f'{url_base}{id}{mod}{self.query}')
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
