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
    URL_BASE = 'https://images.asos-media.com/products/asos'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''extract image id from url'''
        return self.parser.regex_search(r'\d+(?=-\d)', url) or self.parser.regex_search(r'(?<=/)\d{2,}', url)

    def extract_color(self, url):
        '''extract color from url'''
        if 'asos.com' in url:
            color = self.parser.regex_search(r'(?<=clr=)[a-z\s]+', url) \
                    or self.parser.regex_search(r'(?<=-1-)[a-z\s]+', self.get(url).content)
        else:
            color = self.parser.regex_search(r'(?<=-1-)[a-z\d]+', url) \
                    or self.parser.regex_search(r'(?<!/\d/\d)/[a-z\s]+(?=/[^/]+$)', url)

        return color.lstrip('/')

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')

        for target in self.args['targets'][self.ID]:
            color = self.extract_color(target)
            id = self.extract_id(target)

            if color:
                self.collect(f'{self.URL_BASE}/{id}-1-{color}{self.QUERY}')
            for n in range(2, 5):
                self.collect(f'{self.URL_BASE}/{id}-{n}{self.QUERY}')

            self.delay()

        self.loot()
