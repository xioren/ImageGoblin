import re

from goblins.meta import MetaGoblin

# NOTE: removing origin works in some cases, are there different origins?

class HMGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'h&m goblin'
    ID = 'handm'
    URL_PAT = r'source\[[\w\./]+\]'

    def __init__(self, args):
        super().__init__(args)

    def extract_source(self, url):
        '''extract source path from url'''
        return re.search(r'source\[[\w\./]+\]', url).group().replace('source[', '').rstrip(']')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'lp2.hm' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = self.extract_by_regex(self.URL_PAT, target)
            for url in urls:
                source = self.extract_source(url)
                self.collect(f'https://lp2.hm.com/hmgoepprod?set=quality[100],source[{source}],origin[dam]&call=url[file:/product/zoom]',
                             self.parser.extract_filename(source))
        self.loot()
