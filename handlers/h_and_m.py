import re
from handlers.meta_goblin import MetaGoblin

# NOTE: removing origin works in some cases, are there different origins?

class HMGoblin(MetaGoblin):

    '''
    mode options:
        -
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'h&m goblin'

    def extract_source(self, url):
        return re.search(r'source\[[\w\./]+\]', url).group().replace('source[', '').rstrip(']')

    def run(self):
        if 'lp2.hm' in self.args['url']:
            links = [self.args['url']]
        else:
            links = self.extract_links(r'source\[[\w\./]+\]', self.args['url'])
        for link in links:
            source = self.extract_source(link)
            self.collect(f'https://lp2.hm.com/hmgoepprod?set=quality[100],source[{source}],origin[dam]&call=url[file:/product/zoom]',
                         self.extract_filename(source))
        self.loot()
