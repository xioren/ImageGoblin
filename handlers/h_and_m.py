import re
from handlers.meta_goblin import MetaGoblin

# NOTE: removing origin works in some cases, are there different origins?

class HMGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.link_pats = r'source\[[\w\./]+\]'

    def __str__(self):
        return 'h&m goblin'

    def extract_source(self, url):
        return re.search(r'source\[[\w\./]+\]', url).group().replace('source[', '').rstrip(']')

    def run(self):
        if 'lp2.hm' in self.args['url']:
            # NOTE: does not scan
            links = [self.args['url']]
        else:
            links = self.extract_links(self.link_pats, self.args['url'])
        for link in links:
            source = self.extract_source(link)
            self.collect(f'https://lp2.hm.com/hmgoepprod?set=quality[100],source[{source}],origin[dam]&call=url[file:/product/zoom]',
                         self.extract_filename(source))
        self.loot()
