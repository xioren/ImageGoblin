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
        return self.parser.regex_search(r'(?<=/)\d+(?![a-z])', url)

    def extract_name(self, url):
        '''extract profile name'''
        return self.parser.regex_search(fr'(?<={self.BASE_URL})[\w\-]+', url)

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'lisimg' in target:
                self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
                urls.append(target)
            else:
                if 'viewimage' in target:
                    urls.append(f'https://iv1.lisimg.com/image/{self.extract_id(target)}/36800full.jpg')
                else:
                    profile_url = f'{self.BASE_URL}{self.extract_name(target)}/'
                    urls.extend(self.parser.extract_by_regex(self.get(f'{profile_url}pictures/').content, self.URL_PAT))
                    n = 2

                    while True:
                        page_urls = self.parser.extract_by_regex(self.get(f'{profile_url}pictures/{n}').content, self.URL_PAT)
                        if not page_urls:
                            break
                        urls.extend(page_urls)
                        n += 1

            self.delay()

        for url in urls:
            self.collect(self.parser.regex_sub(r'\d+full', '3800full', url), filename=self.extract_id(url))

        self.loot()
