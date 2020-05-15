import re

from goblins.generic_alpha import AlphaGoblin


class ReservedGoblin(AlphaGoblin):

    NAME = 'reserved goblin'
    ID = 'reserved'
    ACCEPT_IMAGE = True
    ACCEPT_WEBPAGE = True

    def __init__(self, args):
        super().__init__(args)

    def generate_urls(self, url, image=True):
        if image:
            return [f'{url[:-5]}{n}.jpg'for n in range(1, 5)]
        else:
            filename = re.search(r'[a-z\d]{5}-[a-z\d]{3}', url).group().upper()
            return ['https://www.reserved.com/media/catalog/product' \
                    f'/{filename[0]}/{filename[1]}/{filename}-00{n}.jpg' for n in range(1, 5)]
