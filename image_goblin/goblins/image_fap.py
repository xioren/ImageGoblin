from goblins.meta import MetaGoblin


class ImageFapGoblin(MetaGoblin):
    '''accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)
        self.url_pat = re.compile(r'https?://cdn\.imagefap\.com/images/full/[^" <]+')

    def __str__(self):
        return 'image fap goblin'

    def __repr__(self):
        return 'imagefap'

    def run(self):
        self.logger.log(1, self.__str__(), 'collecting links')
        for target in self.args['targets'][self.__repr__()]:
            if 'cdn.imagefap' in target:
                urls = [target]
                self.logger.log(1, self.__str__(), 'WARNING', 'image urls not supported')
            else:
                urls = []
                links = self.extract_by_tag(f'{self.parser.dequery(target)}?view=2', 'a', 'href')
                for link in links:
                    if '/photo/' in link:
                        urls.extend(self.extract_by_regex(self.url_pat, f'https://www.imagefap.com{link}'))
            for url in urls:
                self.collect(url)
        self.loot()
