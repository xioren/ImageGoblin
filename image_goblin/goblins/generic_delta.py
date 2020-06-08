import re
import json

from goblins.meta import MetaGoblin


class DeltaGoblin(MetaGoblin):
    '''handles: Inditex Group (_n_n_n)
    accepts:
        - image
        - webpage
    generic backend for:
        - bershka
        - massimodutti
        - oysho
        - pull&bear
        - stradivarius
    '''

    NAME = 'delta goblin'
    ID = 'delta'
    # URL_PAT = r'https?://static[^"]+_\d_\d_\d\.jpe?g'

    def __init__(self, args):
        super().__init__(args)

    def trim(self, url):
        '''remove cropping from query string'''
        return re.sub(r'&imwidth=\d+', '', url)

    def extract_product_id(self, url):
        return re.search(r'(?<=/|p)\d+(?=\.|_)', url).group()

    def run(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if 'photos' in target:
                for mod in self.MODIFIERS:
                    urls.append(self.trim(re.sub(r'_\d+_\d+_\d+', mod, target)))
            else:
                response = json.loads(self.get(self.API_URL.format(self.extract_product_id(target))).content)

                # QUESTION: is it always either or? is the else portion always present?
                if 'bundleProductSummaries' in response and response['bundleProductSummaries']:
                    xmedias = response['bundleProductSummaries'][0]['detail']['xmedia']
                else:
                    xmedias = response['detail']['xmedia']

                for xmedia in xmedias:
                    path = xmedia['path']

                    for xmediaitem in xmedia.get('xmediaItems', ''):
                        for media in xmediaitem.get('medias', ''):
                            urls.append(f'{self.URL_BASE}{path}/{media["idMedia"]}{self.SIZE}.jpg')

            self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
