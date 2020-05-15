import re

from goblins.meta import MetaGoblin


class ListalGoblin(MetaGoblin):
    '''accepts:
        - image*
        - webpage
    '''

    NAME = 'listal goblin'
    ID = 'listal'
    BASE_URL = 'https://www.listal.com/'
    URL_PAT = r'https?://i\d\.lisimg\.com/\d+/\d+full\.jpg'

    def __init__(self, args):
        super().__init__(args)

    def extract_id(self, url):
        '''exract image number'''
        return re.search(r'(?<=/)\d+(?![a-z])', url).group()

    def extract_name(self, url):
        '''extract profile name'''
        return re.search(fr'(?<={self.BASE_URL})[\w\-]+', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting links')
        for target in self.args['targets'][self.ID]:
            if 'lisimg' in target:
                urls = [target]
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
            else:
                urls = []
                if 'viewimage' in target:
                    urls.append(f'https://iv1.lisimg.com/image/{self.extract_id(target)}/36800full.jpg')
                else:
                    profile_url = f'{self.BASE_URL}{self.extract_name(target)}/'
                    urls.extend(self.extract_by_regex(self.URL_PAT, f'{profile_url}pictures/'))
                    n = 2
                    while True:
                        page_urls = self.extract_by_regex(self.URL_PAT, f'{profile_url}pictures/{n}')
                        if not page_urls:
                            break
                        urls.extend(page_urls)
                        n += 1
            for url in urls:
                self.collect(re.sub(r'\d+full', '3800full', url), filename=self.extract_id(url))
        self.loot()
