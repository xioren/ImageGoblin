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
        self.url_pat = fr'https?://[a-z0-9\-]+\.scene7\.com/is/image/[A-Za-z]+/\w+(_\w+)?_\w+'
        self.query = '?fmt=jpeg&qlt=100&scl=1'

    def extract_id(self, url):
        '''extract image id from url'''
        return re.search(r'\w+(_\w+)?(?=_\w+)', url).group()

    def extract_base(self, url):
        '''extract url base'''
        return re.sub(r'(?<=/)[^/]+$', '', url)

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'scene7' in target:
                urls = [self.parser.dequery(target)]
            else:
                if self.accept_webpage:
                    urls = self.extract_urls_greedy(self.url_pat, target)
                else:
                    urls = []
                    if not self.args['silent']:
                        print(f'[{self.__str__()}] <WARNING> webpage urls not supported')
            for url in urls:
                id = self.extract_id(url)
                self.url_base = self.extract_base(url)
                for mod in self.modifiers:
                    self.collect(f'{self.url_base}{id}{mod}{self.query}')
        self.loot()
        self.cleanup(self.path_main)
