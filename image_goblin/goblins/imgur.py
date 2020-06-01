import re

from goblins.meta import MetaGoblin


# misc: '/noscript'
# misc '/embed?pub=true' \s{12}=


class ImgurGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'imgur goblin'
    ID = 'imgur'
    BASE_URL = 'https://i.imgur.com/'

    def __init__(self, args):
        super().__init__(args)


    def clean(self, url):
        return re.sub(r'(/embed|#).+$', '', self.parser.dequery(url))

    def prep(self, url):
        '''upgrade image size'''
        filename  = self.parser.extract_filename(url)

        if len(filename) == 8:
            ext = self.parser.extension(url)
            # IDEA: could skip the len check and just return url[:7]
            url = f'{self.BASE_URL}{filename[:-1]}{ext}'.replace('jpeg', 'jpg')

        return url.replace('m.imgur', 'i.imgur')

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []
        for target in self.args['targets'][self.ID]:
            if 'i.imgur' in target or 'm.imgur' in target:
                urls.append(target)
            elif '/r/' in target:
                matches = self.parser.extract_by_regex(self.get(self.clean(target)).content,
                                                       r'(?<=image\s{15}:\s){[^\n]+}(?=,\n)')
                for match in matches:
                    items = self.parser.load_json(match)
                    urls.append(f'{self.BASE_URL}{items["hash"]}{items["ext"]}')
            else:
                matches = self.parser.extract_by_regex(self.get(self.clean(target)).content,
                                                       r'(?<=image\s{15}:\s){[^\n]+}(?=,\n)')
                for match in matches:
                    items = self.parser.load_json(match)
                    if items['is_album'] == True:
                        for item in items['album_images']['images']:
                            urls.append(f'{self.BASE_URL}{item["hash"]}{item["ext"]}')
                    else:
                        urls.append(f'{self.BASE_URL}{items["hash"]}{items["ext"]}')

                if not urls: # sign in probably required -> try bypass
                    self.logger.log(1, self.NAME, 'attempting bypass')
                    if '/a/' in target:
                        matches = self.parser.extract_by_regex(self.get(f'{self.clean(target)}/embed').content,
                                                               r'(?<=images\s{6}:\s){[^\n]+}(?=,\n)')
                        for match in matches:
                            items = self.parser.load_json(match)

                            for item in items['images']:
                                urls.append(f'{self.BASE_URL}{item["hash"]}{item["ext"]}')
                    else:
                        response = self.get(target)
                        urls.append(re.search(r'(?<=og:image" content=")[^"\?]+', response.content).group())

        for url in urls:
            self.collect(self.prep(url))

        self.loot()
