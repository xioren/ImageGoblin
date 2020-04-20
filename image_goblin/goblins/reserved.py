import re

from goblins.generic_alpha import AlphaGoblin


class ReservedGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.accept_image = True
        self.accept_webpage = True

    def __str__(self):
        return 'reserved goblin'

    def __repr__(self):
        return 'reserved'

    def generate_urls(self, url, image=True):
        if image:
            return [f'{url[:-5]}{n}.jpg'for n in range(1, 5)]
        else:
            filename = re.search(r'[a-z0-9]{5}-[a-z0-9]{3}', url).group().upper()
            return ['https://www.reserved.com/media/catalog/product' \
                    f'/{filename[0]}/{filename[1]}/{filename}-00{n}.jpg' for n in range(1, 5)]
