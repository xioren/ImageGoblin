import re

from goblins.meta import MetaGoblin

# NOTE: removing origin works in some cases, are there different origins?

class HMGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = r'source\[[\w\./]+\]'

    def __str__(self):
        return 'h&m goblin'

    def __repr__(self):
        return 'handm'

    def extract_source(self, url):
        '''extract source path from url'''
        return re.search(r'source\[[\w\./]+\]', url).group().replace('source[', '').rstrip(']')

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'lp2.hm' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not fully supported')
            else:
                urls = self.extract_urls(self.url_pat, target)
            for url in urls:
                source = self.extract_source(url)
                self.collect(f'https://lp2.hm.com/hmgoepprod?set=quality[100],source[{source}],origin[dam]&call=url[file:/product/zoom]',
                             self.extract_filename(source))
        self.loot()
